"use client";

import { cn } from "@/lib/utils";

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  sources?: string[];
}

export function ChatMessage({ message, isUser, sources }: ChatMessageProps) {
  return (
    <div
      className={cn(
        "flex w-full",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={cn(
          "rounded-lg px-4 py-2 max-w-[80%]",
          isUser
            ? "bg-primary-600 text-white"
            : "bg-gray-100 text-gray-900"
        )}
      >
        <p className="whitespace-pre-wrap">{message}</p>
        {!isUser && sources && sources.length > 0 && (
          <div className="mt-2 text-sm">
            <p className="font-semibold text-gray-600">Sources:</p>
            <ul className="list-disc list-inside">
              {sources.map((source, index) => (
                <li key={index} className="text-primary-600">
                  {source}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
} 