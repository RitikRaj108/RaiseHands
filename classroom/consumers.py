"""
WebSocket Consumers for RaiseHand Lite

This module contains the AsyncWebsocketConsumer that handles all
real-time communication between students and teachers.

Key Concepts for Interview:
1. AsyncWebsocketConsumer: Non-blocking async handling of WebSocket connections
2. Channel Groups: Allow broadcasting messages to multiple users at once
3. Message Types: Different event handlers for raise_hand and acknowledge_hand

Flow:
1. User connects → Added to room-specific group
2. Student raises hand → Message broadcast to group
3. Teacher sees update → Can acknowledge/dismiss
4. Acknowledgment → Broadcast to all users in group
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ClassroomConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling classroom interactions.
    
    This consumer handles:
    - Connection/disconnection of students and teachers
    - Raise hand events from students
    - Acknowledge/dismiss hand events from teachers
    
    Each classroom (room_name) has its own channel group, allowing
    multiple classrooms to operate independently.
    """
    
    async def connect(self):
        """
        Called when a WebSocket connection is opened.
        
        1. Extract room name from URL route
        2. Create a unique group name for this room
        3. Add this connection to the room's group
        4. Accept the WebSocket connection
        
        Interview Tip: "Groups allow us to broadcast messages to all
        users in a classroom without maintaining our own connection list."
        """
        # Get room name from URL route (e.g., ws/classroom/room1/)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        
        # Create group name for the channel layer
        # Groups allow broadcasting to all users in the same room
        self.room_group_name = f'classroom_{self.room_name}'
        
        # Get username from URL query params or generate anonymous name
        query_string = self.scope.get('query_string', b'').decode()
        params = dict(param.split('=') for param in query_string.split('&') if '=' in param)
        self.username = params.get('username', f'Anonymous_{id(self)}')
        self.user_type = params.get('type', 'student')  # 'student' or 'teacher'
        
        # Add this channel to the room group
        # This allows receiving broadcasts sent to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Accept the WebSocket connection
        await self.accept()
        
        # Send connection confirmation to the user
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Connected to room: {self.room_name}',
            'username': self.username
        }))
    
    async def disconnect(self, close_code):
        """
        Called when a WebSocket connection is closed.
        
        Clean up by removing this channel from the room group.
        If the user had their hand raised, notify others.
        """
        # Notify group that this user disconnected (hand automatically lowered)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'hand_lowered',
                'student': self.username,
                'reason': 'disconnected'
            }
        )
        
        # Remove this channel from the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """
        Called when a message is received from the WebSocket.
        
        Parses the JSON message and routes to appropriate handler based on type.
        
        Expected message formats:
        - Raise Hand: {"type": "raise_hand", "student": "Name"}
        - Lower Hand: {"type": "lower_hand", "student": "Name"}
        - Acknowledge: {"type": "acknowledge_hand", "student": "Name"}
        - Send Message: {"type": "send_message", "message": "text", "sender": "Name"}
        """
        try:
            # Parse incoming JSON message
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            # Route message to appropriate handler
            if message_type == 'raise_hand':
                # Student is raising their hand
                student = text_data_json.get('student', self.username)
                
                # Broadcast to entire room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'hand_raised',  # This maps to hand_raised() method
                        'student': student
                    }
                )
            
            elif message_type == 'lower_hand':
                # Student is lowering their own hand
                student = text_data_json.get('student', self.username)
                
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'hand_lowered',
                        'student': student,
                        'reason': 'self_lowered'
                    }
                )
            
            elif message_type == 'acknowledge_hand':
                # Teacher is acknowledging/dismissing a raised hand
                student = text_data_json.get('student')
                
                if student:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'hand_acknowledged',  # Maps to hand_acknowledged()
                            'student': student,
                            'acknowledged_by': self.username
                        }
                    )
            
            elif message_type == 'send_message':
                # Chat message from teacher or student
                message = text_data_json.get('message', '')
                sender = text_data_json.get('sender', self.username)
                sender_type = text_data_json.get('sender_type', self.user_type)
                
                if message.strip():  # Only send non-empty messages
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': message,
                            'sender': sender,
                            'sender_type': sender_type
                        }
                    )
            
            elif message_type == 'ping':
                # Keep-alive ping from client
                await self.send(text_data=json.dumps({
                    'type': 'pong'
                }))
        
        except json.JSONDecodeError:
            # Handle invalid JSON
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
    
    # ==========================================================================
    # Event Handlers - These methods are called when group messages are received
    # The method name must match the 'type' field in group_send()
    # ==========================================================================
    
    async def hand_raised(self, event):
        """
        Handler for when a student raises their hand.
        
        Called when 'hand_raised' message is broadcast to the group.
        Sends the update to this WebSocket connection.
        """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'hand_raised',
            'student': event['student']
        }))
    
    async def hand_lowered(self, event):
        """
        Handler for when a student lowers their hand (or disconnects).
        
        Notifies all users that a hand has been lowered.
        """
        await self.send(text_data=json.dumps({
            'type': 'hand_lowered',
            'student': event['student'],
            'reason': event.get('reason', 'unknown')
        }))
    
    async def hand_acknowledged(self, event):
        """
        Handler for when a teacher acknowledges a raised hand.
        
        Called when 'hand_acknowledged' is broadcast to the group.
        The student's UI should update to show their hand was seen.
        
        Interview Tip: "This bidirectional flow shows how WebSockets
        enable true real-time interaction. The student immediately
        knows when the teacher has acknowledged them without polling."
        """
        # Send acknowledgment to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'hand_acknowledged',
            'student': event['student'],
            'acknowledged_by': event.get('acknowledged_by', 'Teacher')
        }))
    
    async def chat_message(self, event):
        """
        Handler for chat messages between teacher and students.
        
        Broadcasts the message to all connected users in the room.
        Messages from teachers are highlighted differently in the UI.
        """
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender': event['sender'],
            'sender_type': event.get('sender_type', 'student')
        }))

