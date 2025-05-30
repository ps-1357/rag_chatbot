"use client";

import { useState } from "react";
import { API_URL } from "@/app/utils/api";
import { ChatMessage } from "../components/ChatMessage";

interface Message {
  message: string;
  isUser: boolean;
  sources?: string[];
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    setIsLoading(true);

    setMessages((prev) => [...prev, { message: userMessage, isUser: true }]);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
          chat_history: [],
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          message: data.response,
          isUser: false,
          sources: data.sources,
        },
      ]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        {
          message: "Sorry, there was an error processing your request.",
          isUser: false,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-4 md:p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-2xl font-bold mb-8 text-center">
          Insurance Plan Assistant
        </h1>

        <div className="flex flex-col space-y-4 mb-4 h-[60vh] overflow-y-auto p-4 border rounded-lg">
          {messages.map((msg, index) => (
            <ChatMessage key={index} {...msg} />
          ))}
          {messages.length === 0 && (
            <p className="text-center text-gray-500">
              Ask me anything about the insurance plans!
            </p>
          )}
        </div>

        <form onSubmit={handleSubmit} className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            disabled={isLoading}
          >
            {isLoading ? "Sending..." : "Send"}
          </button>
        </form>
      </div>
    </main>
  );
} 