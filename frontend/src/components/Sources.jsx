import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

export default function Sources({ sources = [], confidence }) {
  return (
    <aside className="w-80 border-l p-4 bg-muted flex flex-col">
      <h3 className="font-semibold text-sm mb-2">Sources</h3>

      {confidence && (
        <Badge
          className={`mb-3 w-fit text-white ${
            confidence === "high_confidence"
              ? "bg-green-600 hover:bg-green-600"
              : confidence === "medium_confidence"
              ? "bg-yellow-500 hover:bg-yellow-500"
              : "bg-red-600 hover:bg-red-600"
          }`}
        >
          Confidence: {confidence.replace("_", " ")}
        </Badge>
      )}

      <Separator className="mb-3" />

      {sources.length === 0 ? (
        <p className="text-xs text-muted-foreground">
          No sources available for this answer.
        </p>
      ) : (
        <div className="space-y-3 overflow-y-auto">
          {sources.map((s, i) => (
            <Card key={i} className="p-3 text-xs space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-medium">{s.title}</span>
                <Badge variant="outline">
                  {Math.round(s.score * 100)}%
                </Badge>
              </div>

              <p className="text-muted-foreground">
                {s.chunk_text}
              </p>
            </Card>
          ))}
        </div>
      )}
    </aside>
  );
}
