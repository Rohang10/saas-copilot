import { Card } from "@/components/ui/card";

export default function Message({ role, content }) {
  return (
    <div className={`flex ${role === "user" ? "justify-end" : "justify-start"}`}>
      <Card className="max-w-lg p-3 text-sm">
        {content}
      </Card>
    </div>
  );
}
