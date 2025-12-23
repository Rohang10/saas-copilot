import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { LogOut } from "lucide-react";

import Message from "./Message";
import Sources from "./Sources";
import { askQuestion, logout } from "../services/api";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [sources, setSources] = useState([]);
  const [confidence, setConfidence] = useState(null);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const userName = localStorage.getItem("user_name") || "User";

  async function send() {
    if (!question.trim() || loading) return;

    setLoading(true);

    setMessages(prev => [...prev, { role: "user", content: question }]);

    try {
      const res = await askQuestion(question);

      setMessages(prev => [
        ...prev,
        { role: "assistant", content: res.answer },
      ]);

      setSources(res.sources || []);
      setConfidence(res.confidence || null);
    } catch {
      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: "Something went wrong. Please try again.",
        },
      ]);
    } finally {
      setQuestion("");
      setLoading(false);
    }
  }

  function handleLogout() {
    logout();
    window.location.reload();
  }

  return (
    <div className="h-screen flex bg-muted/40">
      {/* Chat section */}
      <div className="flex-1 flex flex-col bg-background shadow-sm">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b">
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleLogout}
              title="Logout"
            >
              <LogOut className="h-5 w-5" />
            </Button>
            <h2 className="text-lg font-semibold">Support Copilot</h2>
          </div>
           <div className="flex items-end gap-3">
              <span className="text-sm font-medium">Hello, {userName}</span>
            </div>
        </div>

        {/* Messages */}
        <div className="flex-1 p-4 space-y-4 overflow-y-auto">
          {messages.map((m, i) => (
            <Message key={i} role={m.role} content={m.content} />
          ))}
        </div>

        {/* Input */}
        <div className="border-t p-4 flex gap-2 bg-background">
          <Input
            value={question}
            placeholder="Ask a question..."
            onChange={e => setQuestion(e.target.value)}
            onKeyDown={e => e.key === "Enter" && send()}
            disabled={loading}
          />
          <Button onClick={send} disabled={loading}>
            {loading ? "Thinking..." : "Send"}
          </Button>
        </div>
      </div>

      {/* Sources panel */}
      <Sources sources={sources} confidence={confidence} />
    </div>
  );
}
