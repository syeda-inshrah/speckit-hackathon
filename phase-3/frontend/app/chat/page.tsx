'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

interface TaskOperation {
  operation: string;
  task_id?: number;
  title?: string;
  description?: string;
  details?: string;
}

export default function ChatPage() {
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isReady, setIsReady] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Get user ID and token from Cookies
    const storedUserId = Cookies.get('user_id');
    const storedToken = Cookies.get('auth_token');

    if (!storedUserId || !storedToken) {
      router.push('/signin');
      return;
    }

    setUserId(storedUserId);
    setToken(storedToken);
    setIsReady(true);
  }, [router]);

  useEffect(() => {
    // Scroll to bottom when messages change
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || !userId || !token || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setIsLoading(true);

    // Add user message to UI immediately
    const tempUserMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: userMessage,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMessage]);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:7860';
      const response = await fetch(`${apiUrl}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          conversation_id: conversationId,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();

      // Debug logging
      console.log('Chat API Response:', data);
      console.log('Message content:', data.message.content);
      console.log('Content length:', data.message.content?.length || 0);

      // Update conversation ID
      if (data.conversation_id && !conversationId) {
        setConversationId(data.conversation_id);
      }

      // Add assistant message
      const assistantMessage: Message = {
        id: data.message.id,
        role: 'assistant',
        content: data.message.content,
        created_at: data.message.created_at,
      };
      setMessages((prev) => [...prev, assistantMessage]);

      // Show task operations if any
      if (data.task_operations && data.task_operations.length > 0) {
        console.log('Task operations:', data.task_operations);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message
      const errorMessage: Message = {
        id: Date.now(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (!isReady) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading chat...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/dashboard')}
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              ← Back to Dashboard
            </button>
            <h1 className="text-2xl font-bold text-gray-900">AI Chat Assistant</h1>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-blue-50 rounded-lg">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
            <span className="text-sm font-medium text-gray-700">
              Powered by OpenAI Agents SDK + MCP
            </span>
          </div>
        </div>
      </div>

      {/* Chat Container */}
      <div className="max-w-4xl mx-auto px-4 py-6">
        <div className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden flex flex-col h-[calc(100vh-200px)]">
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 && (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">👋</div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  Welcome to AI Task Assistant
                </h2>
                <p className="text-gray-600 mb-6">
                  I can help you manage your tasks using natural language!
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
                  {[
                    "Add a task to buy groceries",
                    "Show me all my tasks",
                    "Mark task 1 as complete",
                    "Update task 2 title to 'Finish report'",
                  ].map((example, index) => (
                    <button
                      key={index}
                      onClick={() => setInputMessage(example)}
                      className="text-left p-3 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors text-sm text-gray-700"
                    >
                      "{example}"
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white font-medium'
                      : 'bg-yellow-200 border-2 border-black'
                  }`}
                >
                  <p className={`whitespace-pre-wrap ${
                    message.role === 'user'
                      ? 'text-white'
                      : 'text-black font-bold text-lg'
                  }`}>
                    {message.content || '[EMPTY MESSAGE - NO CONTENT RECEIVED]'}
                  </p>
                  <p
                    className={`text-xs mt-1 ${
                      message.role === 'user' ? 'text-blue-200' : 'text-gray-500'
                    }`}
                  >
                    {new Date(message.created_at).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-2xl px-4 py-3">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 p-4">
            <div className="flex items-end gap-2">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message... (e.g., 'Add a task to buy groceries')"
                className="flex-1 resize-none rounded-xl border border-gray-300 px-4 py-3 text-gray-900 text-base font-medium bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-gray-400"
                rows={1}
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={!inputMessage.trim() || isLoading}
                className="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Help Section */}
      <div className="max-w-4xl mx-auto px-4 py-4">
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">💡 Try these commands:</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {[
              "Add a task to buy groceries",
              "Show me all my tasks",
              "Mark task 1 as complete",
              "Update task 2 title to 'Finish report'",
              "Delete task 3",
              "List my pending tasks",
            ].map((command, index) => (
              <div key={index} className="flex items-start gap-2">
                <span className="text-blue-600">•</span>
                <span className="text-gray-700">"{command}"</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
