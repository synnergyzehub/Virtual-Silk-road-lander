
import { Card, CardContent } from "@/components/ui/card";

const timeline = [
  {
    phase: "Phase 0",
    title: "Vision & Design",
    period: "Months -6 to 0",
    items: [
      "Ideological foundation of trade sovereignty",
      "EmpireOS conceptualized as license engine",
      "ECG established as governance layer",
      "Synergize interface structured",
      "CA firm onboarded for cluster activation"
    ]
  },
  {
    phase: "Phase 1",
    title: "Platform Birth",
    period: "Months 0–3",
    items: [
      "EmpireOS begins license issuance",
      "Synergize interface launches",
      "HSN transaction & scorecard systems go live",
      "Silk Cube token introduced",
      "First clusters activated across India"
    ]
  }
  // Truncated for brevity, more phases can be added
];

export default function EmperorTimeline() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-4xl font-bold">The Reign of the Emperor</h1>
      <p className="text-muted-foreground text-lg">
        A Timeline of Digital Sovereignty through EmpireOS & Synergize
      </p>
      <div className="space-y-4">
        {timeline.map((block) => (
          <Card key={block.phase} className="border-l-4 border-primary">
            <CardContent className="p-6">
              <h2 className="text-2xl font-semibold">{block.phase}: {block.title}</h2>
              <p className="text-sm text-muted-foreground mb-3">{block.period}</p>
              <ul className="list-disc list-inside space-y-1">
                {block.items.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
