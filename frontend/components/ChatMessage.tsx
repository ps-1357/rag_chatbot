interface ChatMessageProps {
  message: string;
  isUser: boolean;
  sources?: string[];
}

export function ChatMessage({ message, isUser, sources }: ChatMessageProps) {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-2 ${
          isUser ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-900'
        }`}
      >
        <p className="whitespace-pre-wrap">{message}</p>
        {sources && sources.length > 0 && (
          <div className="mt-2 text-sm opacity-75">
            <p className="font-semibold">Sources:</p>
            <ul className="list-disc list-inside">
              {sources.map((source, index) => (
                <li key={index} className={isUser ? 'text-white/90' : 'text-gray-600'}>
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