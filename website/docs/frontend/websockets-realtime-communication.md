# Chapter 15: WebSockets - Real-Time Communication
## *Or: How to Stop Polling Your Server Like a Clingy Ex*

> "WebSockets are what happens when HTTP finally admits it's not suited for everything. It's like realizing your bicycle isn't great for cross-country trips." - Every Developer After Their First Real-Time Feature

WebSockets represent the evolutionary leap from "are we there yet?" HTTP polling to "I'll let you know when we arrive" real-time communication. It's the difference between constantly checking your phone for messages and having messages actually push to you like a civilized technology.

## The Polling Problem (And Why It's Terrible)

### Traditional HTTP: The Digital Equivalent of Constantly Asking "Are We There Yet?"

Before WebSockets, implementing real-time features was like having a conversation through written letters. You'd send a request, wait for a response, then immediately send another request asking if anything had changed. Your poor server felt like a call center operator dealing with an anxious relative.

```javascript
// The old way: Polling like a maniac
function pollForUpdates() {
    setInterval(async () => {
        try {
            const response = await fetch('/api/check-for-updates');
            const data = await response.json();
            
            if (data.hasUpdates) {
                updateUI(data);
            }
            
            // Rinse and repeat every 2 seconds
            // Your server is crying
        } catch (error) {
            console.log('Failed to annoy the server');
        }
    }, 2000);
}

// Problems with this approach:
// 1. Constant unnecessary requests (like texting "u up?" every 5 minutes)
// 2. Battery drain on mobile (your phone hates you)
// 3. Server load (your AWS bill also hates you)
// 4. Not actually real-time (2-second delays everywhere)
// 5. Waste of bandwidth (most polls return nothing)
```

### The Resource Drain

**Polling Performance Impact:**
- **100 users polling every 2 seconds**: 50 requests/second
- **1,000 users**: 500 requests/second  
- **10,000 users**: 5,000 requests/second (your server is now on fire)
- **100,000 users**: Time to update your LinkedIn profile

**WebSocket Performance:**
- **100,000 concurrent connections**: 1 persistent connection each
- **Data only when needed**: No empty responses
- **Bidirectional**: Server can initiate communication
- **Low latency**: 1-2ms vs polling's 2000ms average

## Understanding WebSockets: The Simple Version

### The Feynman Explanation

Imagine communication methods as different types of relationships:

**HTTP Requests (Traditional):**
- Like texting someone and waiting for a reply
- Each conversation requires a new text thread
- You can't tell if they're online
- No way to know if they have something to tell you

**WebSocket Connection:**
- Like having a phone call that stays connected
- Either person can talk at any time
- You know immediately when they hang up
- Real-time, bidirectional conversation

**The Handshake:**
```
Browser: "Hey server, want to upgrade our relationship to WebSocket?"
Server: "Sure! Let's do real-time communication."
Both: "Great! Now we can talk whenever we want."
```

### The Technical Reality

WebSockets start as HTTP but upgrade to a persistent TCP connection:

```
1. HTTP Handshake:
   GET /chat HTTP/1.1
   Host: example.com
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
   
2. Server Response:
   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
   
3. Connection Established:
   // Now it's just raw TCP with WebSocket framing
   // No more HTTP overhead
```

## Your First WebSocket Application: Real-Time Chat

Let's build something that actually showcases WebSocket's strengths: a chat application that doesn't suck.

### Backend: Node.js WebSocket Server

**package.json:**
```json
{
  "name": "websocket-chat",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "ws": "^8.14.0",
    "uuid": "^9.0.0"
  },
  "scripts": {
    "start": "node server.js"
  }
}
```

**server.js:**
```javascript
import { WebSocketServer } from 'ws';
import { v4 as uuidv4 } from 'uuid';
import http from 'http';
import { readFileSync } from 'fs';

// Create HTTP server for static files
const server = http.createServer((req, res) => {
    if (req.url === '/' || req.url === '/index.html') {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(readFileSync('./index.html'));
    } else if (req.url === '/chat.js') {
        res.writeHead(200, { 'Content-Type': 'application/javascript' });
        res.end(readFileSync('./chat.js'));
    } else {
        res.writeHead(404);
        res.end('Not found');
    }
});

// Create WebSocket server
const wss = new WebSocketServer({ server });

// Store active connections and rooms
const connections = new Map();
const rooms = new Map();

// Message types for structured communication
const MessageType = {
    JOIN_ROOM: 'join_room',
    LEAVE_ROOM: 'leave_room', 
    CHAT_MESSAGE: 'chat_message',
    USER_LIST: 'user_list',
    SYSTEM_MESSAGE: 'system_message',
    TYPING_START: 'typing_start',
    TYPING_STOP: 'typing_stop'
};

wss.on('connection', (ws, req) => {
    const userId = uuidv4();
    const connectionInfo = {
        id: userId,
        ws: ws,
        rooms: new Set(),
        username: null,
        lastPing: Date.now()
    };
    
    connections.set(userId, connectionInfo);
    
    console.log(`New connection: ${userId} (${connections.size} total)`);
    
    // Send connection confirmation
    ws.send(JSON.stringify({
        type: 'connection_established',
        userId: userId
    }));
    
    ws.on('message', (data) => {
        try {
            const message = JSON.parse(data.toString());
            handleMessage(userId, message);
        } catch (error) {
            console.error('Invalid message:', error);
            ws.send(JSON.stringify({
                type: 'error',
                message: 'Invalid message format'
            }));
        }
    });
    
    ws.on('close', () => {
        handleDisconnection(userId);
    });
    
    ws.on('error', (error) => {
        console.error(`WebSocket error for ${userId}:`, error);
        handleDisconnection(userId);
    });
    
    // Heartbeat to detect dead connections
    ws.on('pong', () => {
        if (connections.has(userId)) {
            connections.get(userId).lastPing = Date.now();
        }
    });
});

function handleMessage(userId, message) {
    const connection = connections.get(userId);
    if (!connection) return;
    
    switch (message.type) {
        case MessageType.JOIN_ROOM:
            joinRoom(userId, message.room, message.username);
            break;
            
        case MessageType.LEAVE_ROOM:
            leaveRoom(userId, message.room);
            break;
            
        case MessageType.CHAT_MESSAGE:
            broadcastChatMessage(userId, message);
            break;
            
        case MessageType.TYPING_START:
            broadcastTypingStatus(userId, message.room, true);
            break;
            
        case MessageType.TYPING_STOP:
            broadcastTypingStatus(userId, message.room, false);
            break;
            
        default:
            console.log('Unknown message type:', message.type);
    }
}

function joinRoom(userId, roomName, username) {
    const connection = connections.get(userId);
    if (!connection) return;
    
    // Initialize room if it doesn't exist
    if (!rooms.has(roomName)) {
        rooms.set(roomName, new Set());
    }
    
    // Add user to room
    rooms.get(roomName).add(userId);
    connection.rooms.add(roomName);
    connection.username = username;
    
    console.log(`${username} joined room: ${roomName}`);
    
    // Notify room about new user
    broadcastToRoom(roomName, {
        type: MessageType.SYSTEM_MESSAGE,
        message: `${username} joined the chat`,
        timestamp: Date.now()
    }, userId);
    
    // Send updated user list to room
    broadcastUserList(roomName);
    
    // Send recent messages to new user (in real app, load from database)
    connection.ws.send(JSON.stringify({
        type: MessageType.SYSTEM_MESSAGE,
        message: `Welcome to ${roomName}!`,
        timestamp: Date.now()
    }));
}

function leaveRoom(userId, roomName) {
    const connection = connections.get(userId);
    if (!connection || !rooms.has(roomName)) return;
    
    rooms.get(roomName).delete(userId);
    connection.rooms.delete(roomName);
    
    // Clean up empty rooms
    if (rooms.get(roomName).size === 0) {
        rooms.delete(roomName);
    } else {
        // Notify remaining users
        broadcastToRoom(roomName, {
            type: MessageType.SYSTEM_MESSAGE,
            message: `${connection.username} left the chat`,
            timestamp: Date.now()
        });
        
        broadcastUserList(roomName);
    }
    
    console.log(`${connection.username} left room: ${roomName}`);
}

function broadcastChatMessage(userId, message) {
    const connection = connections.get(userId);
    if (!connection) return;
    
    const chatMessage = {
        type: MessageType.CHAT_MESSAGE,
        userId: userId,
        username: connection.username,
        message: message.message,
        timestamp: Date.now()
    };
    
    // Broadcast to all rooms the user is in
    connection.rooms.forEach(roomName => {
        broadcastToRoom(roomName, chatMessage);
    });
}

function broadcastTypingStatus(userId, roomName, isTyping) {
    const connection = connections.get(userId);
    if (!connection) return;
    
    const typingMessage = {
        type: isTyping ? MessageType.TYPING_START : MessageType.TYPING_STOP,
        userId: userId,
        username: connection.username,
        room: roomName
    };
    
    broadcastToRoom(roomName, typingMessage, userId);
}

function broadcastToRoom(roomName, message, excludeUserId = null) {
    if (!rooms.has(roomName)) return;
    
    const messageString = JSON.stringify(message);
    
    rooms.get(roomName).forEach(userId => {
        if (userId === excludeUserId) return;
        
        const connection = connections.get(userId);
        if (connection && connection.ws.readyState === connection.ws.OPEN) {
            connection.ws.send(messageString);
        }
    });
}

function broadcastUserList(roomName) {
    if (!rooms.has(roomName)) return;
    
    const users = [];
    rooms.get(roomName).forEach(userId => {
        const connection = connections.get(userId);
        if (connection) {
            users.push({
                id: userId,
                username: connection.username
            });
        }
    });
    
    const userListMessage = {
        type: MessageType.USER_LIST,
        room: roomName,
        users: users
    };
    
    broadcastToRoom(roomName, userListMessage);
}

function handleDisconnection(userId) {
    const connection = connections.get(userId);
    if (!connection) return;
    
    console.log(`Connection closed: ${userId}`);
    
    // Remove from all rooms
    connection.rooms.forEach(roomName => {
        leaveRoom(userId, roomName);
    });
    
    connections.delete(userId);
}

// Heartbeat to remove dead connections
setInterval(() => {
    const now = Date.now();
    connections.forEach((connection, userId) => {
        if (now - connection.lastPing > 30000) { // 30 seconds timeout
            console.log(`Removing dead connection: ${userId}`);
            connection.ws.terminate();
            handleDisconnection(userId);
        } else {
            // Send ping
            if (connection.ws.readyState === connection.ws.OPEN) {
                connection.ws.ping();
            }
        }
    });
}, 15000); // Check every 15 seconds

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
```

### Frontend: JavaScript WebSocket Client

**index.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 WebSocket Chat</title>
    <style>
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        
        .chat-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .chat-header {
            background: #007bff;
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .connection-status {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #28a745;
        }
        
        .status-dot.disconnected {
            background: #dc3545;
        }
        
        .chat-messages {
            height: 400px;
            overflow-y: auto;
            padding: 20px;
            background: #fafafa;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
        }
        
        .message.own {
            background: #007bff;
            color: white;
            margin-left: 50px;
        }
        
        .message.other {
            background: white;
            margin-right: 50px;
            border: 1px solid #eee;
        }
        
        .message.system {
            background: #f8f9fa;
            color: #6c757d;
            text-align: center;
            font-style: italic;
            margin: 5px 0;
        }
        
        .message-header {
            font-size: 0.8em;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        
        .typing-indicator {
            color: #6c757d;
            font-style: italic;
            padding: 5px 20px;
        }
        
        .chat-input {
            display: flex;
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
        }
        
        .chat-input input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-right: 10px;
        }
        
        .chat-input button {
            padding: 10px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .user-list {
            background: white;
            padding: 15px;
            margin-top: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .join-form {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .join-form input {
            display: block;
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        
        .join-form button {
            background: #28a745;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        
        .performance-stats {
            background: #f8f9fa;
            padding: 10px;
            margin-top: 20px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 0.9em;
        }
        
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <h1>🚀 WebSocket Real-Time Chat</h1>
    <p>Experience the magic of real-time communication without the pain of polling!</p>
    
    <!-- Join Form -->
    <div id="join-form" class="join-form">
        <h2>Join the Chat</h2>
        <input type="text" id="username" placeholder="Your username" maxlength="20">
        <input type="text" id="room" placeholder="Room name" value="general" maxlength="30">
        <button onclick="joinChat()">Join Chat</button>
    </div>
    
    <!-- Chat Interface -->
    <div id="chat-interface" class="hidden">
        <div class="chat-container">
            <div class="chat-header">
                <h2 id="room-title">Chat Room</h2>
                <div class="connection-status">
                    <span class="status-dot" id="status-dot"></span>
                    <span id="connection-status">Connected</span>
                </div>
            </div>
            
            <div class="chat-messages" id="chat-messages"></div>
            
            <div class="typing-indicator" id="typing-indicator"></div>
            
            <div class="chat-input">
                <input 
                    type="text" 
                    id="message-input" 
                    placeholder="Type your message..." 
                    maxlength="500"
                    onkeypress="handleKeyPress(event)"
                    oninput="handleTyping()"
                >
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
        
        <div class="user-list">
            <h3>Online Users</h3>
            <div id="user-list"></div>
        </div>
        
        <div class="performance-stats">
            <div>Messages sent: <span id="messages-sent">0</span></div>
            <div>Messages received: <span id="messages-received">0</span></div>
            <div>Connection uptime: <span id="uptime">0s</span></div>
            <div>Last message latency: <span id="latency">-</span></div>
        </div>
        
        <button onclick="leaveChat()" style="margin-top: 20px; padding: 10px 20px; background: #dc3545; color: white; border: none; border-radius: 5px;">
            Leave Chat
        </button>
    </div>
    
    <script src="chat.js"></script>
</body>
</html>
```

**chat.js:**
```javascript
class WebSocketChat {
    constructor() {
        this.ws = null;
        this.userId = null;
        this.username = null;
        this.currentRoom = null;
        this.isConnected = false;
        this.typingTimeout = null;
        this.isTyping = false;
        this.messagesSent = 0;
        this.messagesReceived = 0;
        this.connectionTime = null;
        this.performanceStats = {};
        
        this.initializePerformanceTracking();
    }
    
    connect() {
        // Use wss:// for HTTPS sites, ws:// for HTTP
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.isConnected = true;
            this.connectionTime = Date.now();
            this.updateConnectionStatus(true);
        };
        
        this.ws.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                this.handleMessage(message);
                this.messagesReceived++;
                this.updatePerformanceStats();
            } catch (error) {
                console.error('Failed to parse message:', error);
            }
        };
        
        this.ws.onclose = (event) => {
            console.log('WebSocket closed:', event.code, event.reason);
            this.isConnected = false;
            this.updateConnectionStatus(false);
            
            // Attempt to reconnect after a delay
            if (this.currentRoom) {
                setTimeout(() => {
                    console.log('Attempting to reconnect...');
                    this.connect();
                }, 3000);
            }
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus(false);
        };
    }
    
    handleMessage(message) {
        // Calculate latency for performance tracking
        if (message.timestamp) {
            const latency = Date.now() - message.timestamp;
            this.performanceStats.lastLatency = latency;
        }
        
        switch (message.type) {
            case 'connection_established':
                this.userId = message.userId;
                break;
                
            case 'chat_message':
                this.displayChatMessage(message);
                break;
                
            case 'system_message':
                this.displaySystemMessage(message.message);
                break;
                
            case 'user_list':
                this.updateUserList(message.users);
                break;
                
            case 'typing_start':
                this.showTypingIndicator(message.username);
                break;
                
            case 'typing_stop':
                this.hideTypingIndicator(message.username);
                break;
                
            case 'error':
                console.error('Server error:', message.message);
                this.displaySystemMessage(`Error: ${message.message}`);
                break;
                
            default:
                console.log('Unknown message type:', message.type);
        }
    }
    
    joinRoom(username, room) {
        this.username = username;
        this.currentRoom = room;
        
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
            this.connect();
            
            // Wait for connection before joining
            const waitForConnection = () => {
                if (this.ws.readyState === WebSocket.OPEN) {
                    this.sendMessage({
                        type: 'join_room',
                        room: room,
                        username: username
                    });
                } else {
                    setTimeout(waitForConnection, 100);
                }
            };
            
            waitForConnection();
        } else {
            this.sendMessage({
                type: 'join_room',
                room: room,
                username: username
            });
        }
        
        // Update UI
        document.getElementById('room-title').textContent = `#${room}`;
        this.clearMessages();
    }
    
    leaveRoom() {
        if (this.currentRoom) {
            this.sendMessage({
                type: 'leave_room',
                room: this.currentRoom
            });
        }
        
        if (this.ws) {
            this.ws.close();
        }
        
        this.currentRoom = null;
        this.username = null;
        this.userId = null;
    }
    
    sendChatMessage(messageText) {
        if (!messageText.trim()) return;
        
        const message = {
            type: 'chat_message',
            message: messageText.trim(),
            timestamp: Date.now() // For latency calculation
        };
        
        this.sendMessage(message);
        this.messagesSent++;
        this.updatePerformanceStats();
        
        // Stop typing indicator
        this.stopTyping();
    }
    
    sendMessage(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        } else {
            console.error('WebSocket not connected');
            this.displaySystemMessage('Connection lost. Trying to reconnect...');
        }
    }
    
    startTyping() {
        if (!this.isTyping && this.currentRoom) {
            this.isTyping = true;
            this.sendMessage({
                type: 'typing_start',
                room: this.currentRoom
            });
        }
        
        // Reset typing timeout
        clearTimeout(this.typingTimeout);
        this.typingTimeout = setTimeout(() => {
            this.stopTyping();
        }, 3000);
    }
    
    stopTyping() {
        if (this.isTyping && this.currentRoom) {
            this.isTyping = false;
            this.sendMessage({
                type: 'typing_stop',
                room: this.currentRoom
            });
        }
        
        clearTimeout(this.typingTimeout);
    }
    
    displayChatMessage(message) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        
        const isOwnMessage = message.userId === this.userId;
        messageDiv.className = `message ${isOwnMessage ? 'own' : 'other'}`;
        
        const timestamp = new Date(message.timestamp).toLocaleTimeString();
        
        messageDiv.innerHTML = `
            <div class="message-header">
                ${message.username} • ${timestamp}
            </div>
            <div>${this.escapeHtml(message.message)}</div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    displaySystemMessage(messageText) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message system';
        messageDiv.textContent = messageText;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    updateUserList(users) {
        const userListContainer = document.getElementById('user-list');
        userListContainer.innerHTML = users.map(user => 
            `<div>${this.escapeHtml(user.username)} ${user.id === this.userId ? '(you)' : ''}</div>`
        ).join('');
    }
    
    showTypingIndicator(username) {
        const indicator = document.getElementById('typing-indicator');
        const currentText = indicator.textContent;
        
        if (!currentText.includes(username)) {
            const typingUsers = currentText ? currentText.split(' and ') : [];
            typingUsers.push(username);
            indicator.textContent = `${typingUsers.join(' and ')} typing...`;
        }
    }
    
    hideTypingIndicator(username) {
        const indicator = document.getElementById('typing-indicator');
        const currentText = indicator.textContent;
        
        if (currentText.includes(username)) {
            const typingUsers = currentText.split(' and ')
                .map(s => s.replace(' typing...', ''))
                .filter(s => s !== username && s !== '');
            
            indicator.textContent = typingUsers.length > 0 ? 
                `${typingUsers.join(' and ')} typing...` : '';
        }
    }
    
    updateConnectionStatus(connected) {
        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('connection-status');
        
        if (connected) {
            statusDot.classList.remove('disconnected');
            statusText.textContent = 'Connected';
        } else {
            statusDot.classList.add('disconnected');
            statusText.textContent = 'Disconnected';
        }
    }
    
    clearMessages() {
        document.getElementById('chat-messages').innerHTML = '';
        document.getElementById('typing-indicator').textContent = '';
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    initializePerformanceTracking() {
        setInterval(() => {
            this.updatePerformanceStats();
        }, 1000);
    }
    
    updatePerformanceStats() {
        document.getElementById('messages-sent').textContent = this.messagesSent;
        document.getElementById('messages-received').textContent = this.messagesReceived;
        
        if (this.connectionTime) {
            const uptime = Math.floor((Date.now() - this.connectionTime) / 1000);
            document.getElementById('uptime').textContent = `${uptime}s`;
        }
        
        if (this.performanceStats.lastLatency !== undefined) {
            document.getElementById('latency').textContent = `${this.performanceStats.lastLatency}ms`;
        }
    }
}

// Global chat instance
const chat = new WebSocketChat();

// UI Event Handlers
function joinChat() {
    const username = document.getElementById('username').value.trim();
    const room = document.getElementById('room').value.trim();
    
    if (!username || !room) {
        alert('Please enter both username and room name');
        return;
    }
    
    chat.joinRoom(username, room);
    
    // Show chat interface
    document.getElementById('join-form').classList.add('hidden');
    document.getElementById('chat-interface').classList.remove('hidden');
    
    // Focus message input
    document.getElementById('message-input').focus();
}

function leaveChat() {
    chat.leaveRoom();
    
    // Show join form
    document.getElementById('chat-interface').classList.add('hidden');
    document.getElementById('join-form').classList.remove('hidden');
    
    // Reset form
    document.getElementById('username').value = '';
    document.getElementById('room').value = 'general';
}

function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (message) {
        chat.sendChatMessage(message);
        input.value = '';
    }
    
    input.focus();
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function handleTyping() {
    chat.startTyping();
}

// Handle page unload
window.addEventListener('beforeunload', () => {
    chat.leaveRoom();
});
```

## Advanced WebSocket Patterns

### Authentication and Authorization

```javascript
// Server-side authentication middleware
function authenticateWebSocket(ws, req, next) {
    const token = new URL(req.url, 'http://localhost').searchParams.get('token');
    
    if (!token) {
        ws.close(4001, 'Authentication required');
        return;
    }
    
    try {
        const user = verifyJWT(token);
        req.user = user;
        next();
    } catch (error) {
        ws.close(4001, 'Invalid token');
    }
}

// Client-side authentication
class AuthenticatedWebSocket {
    constructor(token) {
        this.token = token;
    }
    
    connect() {
        const wsUrl = `ws://localhost:3000?token=${this.token}`;
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            console.log('Authenticated connection established');
        };
        
        this.ws.onclose = (event) => {
            if (event.code === 4001) {
                console.error('Authentication failed');
                // Redirect to login
            }
        };
    }
}
```

### Rate Limiting and Abuse Prevention

```javascript
// Server-side rate limiting
class RateLimiter {
    constructor() {
        this.clients = new Map();
    }
    
    isAllowed(userId, maxRequests = 10, windowMs = 60000) {
        const now = Date.now();
        const client = this.clients.get(userId) || { requests: [], banned: false };
        
        if (client.banned) {
            return false;
        }
        
        // Remove old requests outside the window
        client.requests = client.requests.filter(time => now - time < windowMs);
        
        if (client.requests.length >= maxRequests) {
            client.banned = true;
            setTimeout(() => {
                client.banned = false;
                client.requests = [];
            }, windowMs * 2); // Ban for 2x the window
            
            return false;
        }
        
        client.requests.push(now);
        this.clients.set(userId, client);
        return true;
    }
}

const rateLimiter = new RateLimiter();

// Use in message handler
function handleMessage(userId, message) {
    if (!rateLimiter.isAllowed(userId)) {
        const connection = connections.get(userId);
        if (connection) {
            connection.ws.send(JSON.stringify({
                type: 'error',
                message: 'Rate limit exceeded. Please slow down.'
            }));
        }
        return;
    }
    
    // Process message normally
}
```

### Graceful Error Handling and Reconnection

```javascript
class RobustWebSocket {
    constructor(url, options = {}) {
        this.url = url;
        this.options = {
            reconnectInterval: 1000,
            maxReconnectAttempts: 10,
            reconnectBackoff: 1.5,
            ...options
        };
        
        this.reconnectAttempts = 0;
        this.shouldReconnect = true;
        this.messageQueue = [];
        
        this.connect();
    }
    
    connect() {
        try {
            this.ws = new WebSocket(this.url);
            
            this.ws.onopen = () => {
                console.log('WebSocket connected');
                this.reconnectAttempts = 0;
                this.flushMessageQueue();
                this.onopen?.();
            };
            
            this.ws.onmessage = (event) => {
                this.onmessage?.(event);
            };
            
            this.ws.onclose = (event) => {
                console.log('WebSocket closed:', event.code);
                this.onclose?.(event);
                
                if (this.shouldReconnect && this.reconnectAttempts < this.options.maxReconnectAttempts) {
                    this.scheduleReconnect();
                }
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.onerror?.(error);
            };
            
        } catch (error) {
            console.error('Failed to create WebSocket:', error);
            this.scheduleReconnect();
        }
    }
    
    scheduleReconnect() {
        const delay = this.options.reconnectInterval * 
                     Math.pow(this.options.reconnectBackoff, this.reconnectAttempts);
        
        console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts + 1})`);
        
        setTimeout(() => {
            this.reconnectAttempts++;
            this.connect();
        }, delay);
    }
    
    send(data) {
        if (this.ws?.readyState === WebSocket.OPEN) {
            this.ws.send(data);
        } else {
            // Queue message for when connection is restored
            this.messageQueue.push(data);
        }
    }
    
    flushMessageQueue() {
        while (this.messageQueue.length > 0) {
            const message = this.messageQueue.shift();
            this.ws.send(message);
        }
    }
    
    close() {
        this.shouldReconnect = false;
        this.ws?.close();
    }
}
```

## Performance Optimization Strategies

### Message Compression and Batching

```javascript
// Server-side message batching
class MessageBatcher {
    constructor(batchSize = 10, flushInterval = 50) {
        this.batches = new Map();
        this.batchSize = batchSize;
        this.flushInterval = flushInterval;
        
        setInterval(() => {
            this.flushAllBatches();
        }, flushInterval);
    }
    
    addMessage(roomName, message) {
        if (!this.batches.has(roomName)) {
            this.batches.set(roomName, []);
        }
        
        const batch = this.batches.get(roomName);
        batch.push(message);
        
        if (batch.length >= this.batchSize) {
            this.flushBatch(roomName);
        }
    }
    
    flushBatch(roomName) {
        const batch = this.batches.get(roomName);
        if (!batch || batch.length === 0) return;
        
        const batchMessage = {
            type: 'message_batch',
            messages: batch,
            room: roomName
        };
        
        broadcastToRoom(roomName, batchMessage);
        this.batches.set(roomName, []);
    }
    
    flushAllBatches() {
        this.batches.forEach((_, roomName) => {
            this.flushBatch(roomName);
        });
    }
}

// Client-side batch processing
function handleMessageBatch(batchMessage) {
    batchMessage.messages.forEach(message => {
        processMessage(message);
    });
}
```

### Binary Data and Protocol Optimization

```javascript
// Custom binary protocol for high-frequency data
class BinaryWebSocket {
    constructor(url) {
        this.ws = new WebSocket(url);
        this.ws.binaryType = 'arraybuffer';
        
        this.ws.onmessage = (event) => {
            if (event.data instanceof ArrayBuffer) {
                this.handleBinaryMessage(event.data);
            } else {
                this.handleTextMessage(event.data);
            }
        };
    }
    
    sendBinaryMessage(type, data) {
        const buffer = new ArrayBuffer(1 + data.byteLength);
        const view = new DataView(buffer);
        
        view.setUint8(0, type); // Message type
        new Uint8Array(buffer, 1).set(new Uint8Array(data));
        
        this.ws.send(buffer);
    }
    
    handleBinaryMessage(buffer) {
        const view = new DataView(buffer);
        const type = view.getUint8(0);
        const data = buffer.slice(1);
        
        switch (type) {
            case 1: // Position update
                this.handlePositionUpdate(data);
                break;
            case 2: // Bulk data
                this.handleBulkData(data);
                break;
        }
    }
    
    sendPositionUpdate(x, y, z) {
        const buffer = new ArrayBuffer(12);
        const view = new DataView(buffer);
        
        view.setFloat32(0, x);
        view.setFloat32(4, y);
        view.setFloat32(8, z);
        
        this.sendBinaryMessage(1, buffer);
    }
}
```

## Production Deployment Considerations

### Load Balancing WebSocket Connections

```javascript
// Redis adapter for multi-server scaling
const redis = require('redis');
const { createAdapter } = require('@socket.io/redis-adapter');

const pubClient = redis.createClient({ host: 'localhost', port: 6379 });
const subClient = pubClient.duplicate();

io.adapter(createAdapter(pubClient, subClient));

// Sticky session configuration (nginx)
/*
upstream websocket_backend {
    ip_hash; # Sticky sessions
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
}

server {
    location /socket.io/ {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
*/
```

### Monitoring and Metrics

```javascript
// WebSocket metrics collection
class WebSocketMetrics {
    constructor() {
        this.metrics = {
            totalConnections: 0,
            activeConnections: 0,
            messagesPerSecond: 0,
            averageLatency: 0,
            errorRate: 0
        };
        
        this.messageCount = 0;
        this.latencySum = 0;
        this.latencyCount = 0;
        this.errorCount = 0;
        
        setInterval(() => {
            this.calculateMetrics();
            this.reportMetrics();
        }, 10000); // Report every 10 seconds
    }
    
    recordConnection() {
        this.metrics.totalConnections++;
        this.metrics.activeConnections++;
    }
    
    recordDisconnection() {
        this.metrics.activeConnections = Math.max(0, this.metrics.activeConnections - 1);
    }
    
    recordMessage(latency) {
        this.messageCount++;
        if (latency) {
            this.latencySum += latency;
            this.latencyCount++;
        }
    }
    
    recordError() {
        this.errorCount++;
    }
    
    calculateMetrics() {
        this.metrics.messagesPerSecond = this.messageCount / 10;
        this.metrics.averageLatency = this.latencyCount > 0 ? 
            this.latencySum / this.latencyCount : 0;
        this.metrics.errorRate = this.errorCount / (this.messageCount + this.errorCount);
        
        // Reset counters
        this.messageCount = 0;
        this.latencySum = 0;
        this.latencyCount = 0;
        this.errorCount = 0;
    }
    
    reportMetrics() {
        console.log('WebSocket Metrics:', this.metrics);
        
        // Send to monitoring service
        // sendToDatadog(this.metrics);
        // sendToPrometheus(this.metrics);
    }
}
```

## When to Use WebSockets (And When Not To)

### Perfect WebSocket Use Cases ✅

**Real-Time Collaboration:**
```javascript
// Google Docs-style collaborative editing
function handleDocumentChange(change) {
    // Broadcast change to all connected users
    broadcastToRoom(documentId, {
        type: 'document_change',
        change: change,
        userId: currentUser.id,
        timestamp: Date.now()
    });
}
```

**Live Data Feeds:**
```javascript
// Stock prices, sports scores, IoT sensor data
function broadcastPriceUpdate(symbol, price) {
    subscribedUsers.get(symbol).forEach(userId => {
        sendToUser(userId, {
            type: 'price_update',
            symbol: symbol,
            price: price,
            timestamp: Date.now()
        });
    });
}
```

**Gaming and Real-Time Applications:**
```javascript
// Multiplayer game state synchronization
function broadcastPlayerPosition(playerId, position) {
    gameRoom.players.forEach(player => {
        if (player.id !== playerId) {
            sendToPlayer(player.id, {
                type: 'player_moved',
                playerId: playerId,
                position: position
            });
        }
    });
}
```

### Terrible WebSocket Use Cases ❌

**Simple Form Submissions:**
```javascript
// Don't do this - just use regular HTTP
function submitForm(formData) {
    ws.send(JSON.stringify({
        type: 'form_submit',
        data: formData
    }));
}

// Better:
async function submitForm(formData) {
    const response = await fetch('/api/submit', {
        method: 'POST',
        body: formData
    });
    return response.json();
}
```

**File Uploads:**
```javascript
// WebSockets aren't designed for large binary transfers
// Use regular HTTP with progress tracking instead
```

**One-Way Notifications:**
```javascript
// If you only need server-to-client notifications,
// consider Server-Sent Events (SSE) instead
const eventSource = new EventSource('/api/notifications');
eventSource.onmessage = (event) => {
    const notification = JSON.parse(event.data);
    showNotification(notification);
};
```

## The Future of WebSockets

### WebRTC for Peer-to-Peer Communication

```javascript
// WebRTC for direct browser-to-browser communication
class P2PChat {
    constructor() {
        this.peerConnection = new RTCPeerConnection({
            iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
        });
        
        this.dataChannel = this.peerConnection.createDataChannel('chat');
        this.dataChannel.onopen = () => console.log('P2P channel open');
        this.dataChannel.onmessage = (event) => this.handleMessage(event.data);
    }
    
    sendMessage(message) {
        if (this.dataChannel.readyState === 'open') {
            this.dataChannel.send(message);
        }
    }
}
```

### HTTP/3 and QUIC

```javascript
// Future: WebTransport for low-latency, multiplexed communication
const transport = new WebTransport('https://example.com:4433/webtransport');

await transport.ready;

const stream = await transport.createSendStream();
const writer = stream.writable.getWriter();
await writer.write(new TextEncoder().encode('Hello, WebTransport!'));
```

## Conclusion: Real-Time Done Right

WebSockets solve a specific problem: bidirectional, real-time communication between browser and server. They're not a replacement for HTTP—they're a specialized tool for specific use cases.

**The Golden Rules of WebSocket Usage:**
1. **Use for real-time, bidirectional communication only**
2. **Plan for connection failures and reconnection**
3. **Implement proper authentication and rate limiting**
4. **Monitor performance and scale appropriately**
5. **Consider alternatives like SSE for one-way communication**

**The WebSocket Sweet Spots:**
- **Chat applications**: Real-time messaging
- **Live updates**: Stock prices, sports scores, notifications
- **Collaborative tools**: Document editing, shared whiteboards
- **Gaming**: Multiplayer state synchronization
- **IoT dashboards**: Real-time sensor data

Remember: WebSockets are a tool, not a silver bullet. Use them when you need real-time bidirectional communication, skip them when regular HTTP will do, and always measure performance rather than assuming.

The goal isn't to use the coolest technology—it's to provide the best user experience with the simplest solution that works.

---

*"WebSockets: Because sometimes you need to talk to your server in real-time, not send it a letter and wait for a response like it's 1995."* - Modern Web Development Wisdom

*"HTTP: 'Are we there yet?' WebSockets: 'I'll let you know when we arrive.'"* - The Evolution of Web Communication

## Practical Exercises

1. **Performance Comparison**: Implement the same real-time feature using polling, Server-Sent Events, and WebSockets. Measure resource usage and user experience.

2. **Resilient Connection**: Build a WebSocket client that gracefully handles network interruptions, server restarts, and maintains state across reconnections.

3. **Scale Testing**: Create a simple chat application and test how many concurrent connections your server can handle. Identify bottlenecks.

4. **Security Audit**: Implement authentication, rate limiting, and input validation for a WebSocket application. Test it against common attack vectors.

5. **Real-World Integration**: Add real-time features to an existing application. Document the decision process of when to use WebSockets vs alternatives.