"use client";

import { useState } from "react";
import { Cat } from "lucide-react";

import { Chat } from "@/components/chat";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const ASSISTANTS = [
  { id: "simple_agent", name: "Simple Agent" },
  { id: "agent_with_helpfulness", name: "Agent with Helpfulness" },
];

export default function Page() {
  const [assistantId, setAssistantId] = useState(ASSISTANTS[0].id);

  return (
    <main className="flex h-dvh flex-col">
      <header className="border-b bg-background">
        <div className="mx-auto flex w-full max-w-3xl items-center gap-2 px-4 py-3">
          <div className="flex size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Cat className="size-4" />
          </div>
          <div className="leading-tight">
            <p className="text-sm font-medium">Cat Health Agent</p>
            <p className="text-xs text-muted-foreground">LangGraph + Next.js</p>
          </div>

          <div className="ml-auto">
            <Select
              value={assistantId}
              onValueChange={(value) => value && setAssistantId(value)}
            >
              <SelectTrigger size="sm" className="w-52">
                <SelectValue>
                  {(value: string | null) =>
                    ASSISTANTS.find((a) => a.id === value)?.name ?? value
                  }
                </SelectValue>
              </SelectTrigger>
              <SelectContent>
                {ASSISTANTS.map((a) => (
                  <SelectItem key={a.id} value={a.id}>
                    {a.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
      </header>

      <Chat key={assistantId} assistantId={assistantId} />
    </main>
  );
}
