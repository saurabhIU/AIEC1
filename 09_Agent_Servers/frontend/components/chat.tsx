"use client";

import { useStream } from "@langchain/react";
import { Bot, FileText, Loader2, Search, Wrench } from "lucide-react";

import {
  Conversation,
  ConversationContent,
  ConversationScrollButton,
} from "@/components/ai-elements/conversation";
import {
  Message,
  MessageContent,
  MessageResponse,
} from "@/components/ai-elements/message";
import {
  PromptInput,
  PromptInputBody,
  PromptInputFooter,
  PromptInputSubmit,
  PromptInputTextarea,
  type PromptInputMessage,
} from "@/components/ai-elements/prompt-input";
import { Suggestion, Suggestions } from "@/components/ai-elements/suggestion";
import {
  Tool,
  ToolContent,
  ToolHeader,
  ToolOutput,
} from "@/components/ai-elements/tool";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { getMessageText, toolLabel } from "@/lib/messages";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "/api";

type StreamMessage = ReturnType<typeof useStream>["messages"][number];

const SUGGESTIONS = [
  "How often should I deworm my cat?",
  "What vaccinations do kittens need?",
  "What are signs of feline dehydration?",
];

function toolIcon(name?: string) {
  if (name === "retrieve_information") return <FileText className="size-3" />;
  if (name?.startsWith("tavily")) return <Search className="size-3" />;
  return <Wrench className="size-3" />;
}

function roleFrom(type: string): "user" | "assistant" {
  return type === "human" ? "user" : "assistant";
}

export function Chat({ assistantId }: { assistantId: string }) {
  const stream = useStream({ apiUrl: API_URL, assistantId });
  const { messages, isLoading, error } = stream;

  const send = (text: string) => {
    const content = text.trim();
    if (!content || isLoading) return;
    stream.submit({ messages: [{ type: "human", content }] });
  };

  const onSubmit = (message: PromptInputMessage) => {
    send(message.text);
  };

  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <Conversation className="flex-1">
        <ConversationContent className="mx-auto w-full max-w-3xl gap-6">
          {messages.length === 0 && (
            <div className="mt-10 flex flex-col items-center gap-6 text-center">
              <div className="flex size-14 items-center justify-center rounded-full bg-muted">
                <Bot className="size-7 text-muted-foreground" />
              </div>
              <div className="space-y-1">
                <h2 className="text-lg font-medium">Ask the cat health agent</h2>
                <p className="text-sm text-muted-foreground">
                  Streams from your LangGraph deployment via a secure proxy.
                </p>
              </div>
              <Suggestions className="justify-center">
                {SUGGESTIONS.map((s) => (
                  <Suggestion key={s} suggestion={s} onClick={send} />
                ))}
              </Suggestions>
            </div>
          )}

          {messages.map((message, i) => (
            <MessageRow key={message.id ?? i} message={message} />
          ))}

          {isLoading && <ThinkingRow />}

          {error != null && (
            <Card className="border-destructive/40">
              <CardContent className="text-sm text-destructive">
                {error instanceof Error ? error.message : "Something went wrong."}
              </CardContent>
            </Card>
          )}
        </ConversationContent>
        <ConversationScrollButton />
      </Conversation>

      <div className="border-t bg-background">
        <div className="mx-auto w-full max-w-3xl px-4 py-3">
          <PromptInput onSubmit={onSubmit}>
            <PromptInputBody>
              <PromptInputTextarea
                placeholder="Message the agent..."
                disabled={isLoading}
                autoFocus
              />
            </PromptInputBody>
            <PromptInputFooter>
              <PromptInputSubmit
                status={isLoading ? "submitted" : undefined}
                disabled={isLoading}
              />
            </PromptInputFooter>
          </PromptInput>
        </div>
      </div>
    </div>
  );
}

function MessageRow({ message }: { message: StreamMessage }) {
  const text = getMessageText(message.content);

  if (message.type === "tool") {
    return (
      <Tool>
        <ToolHeader
          type="dynamic-tool"
          state="output-available"
          toolName={toolLabel(message.name)}
        />
        <ToolContent>
          <ToolOutput output={text} errorText={undefined} />
        </ToolContent>
      </Tool>
    );
  }

  const toolCalls =
    message.type === "ai"
      ? (message as unknown as {
          tool_calls?: Array<{ name?: string; id?: string }>;
        }).tool_calls ?? []
      : [];

  if (!text && toolCalls.length === 0) return null;

  return (
    <Message from={roleFrom(message.type)}>
      <MessageContent>
        {toolCalls.length > 0 && (
          <div className="flex flex-wrap gap-1.5">
            {toolCalls.map((tc, idx) => (
              <Badge key={tc.id ?? idx} variant="secondary" className="gap-1">
                {toolIcon(tc.name)}
                {toolLabel(tc.name)}
              </Badge>
            ))}
          </div>
        )}
        {text && <MessageResponse>{text}</MessageResponse>}
      </MessageContent>
    </Message>
  );
}

function ThinkingRow() {
  return (
    <Message from="assistant">
      <MessageContent>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Loader2 className="size-4 animate-spin" />
          Thinking...
        </div>
      </MessageContent>
    </Message>
  );
}
