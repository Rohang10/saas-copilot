import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { login } from "../services/api";

export default function Login({ onSuccess }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleLogin() {
    const res = await login(email, password);
    if (res.access_token) onSuccess();
  }

  return (
    <Card className="w-full max-w-sm">
      <CardHeader className="text-lg font-semibold">Login</CardHeader>
      <CardContent className="space-y-4">
        <Input placeholder="Email" onChange={e => setEmail(e.target.value)} />
        <Input
          type="password"
          placeholder="Password"
          onChange={e => setPassword(e.target.value)}
        />
        <Button className="w-full" onClick={handleLogin}>
          Sign In
        </Button>
      </CardContent>
    </Card>
  );
}
