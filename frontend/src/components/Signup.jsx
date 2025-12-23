import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { signup } from "../services/api";

export default function Signup({ onSuccess }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [name, setName] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSignup(e) {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            await signup(name, email, password);
            onSuccess(); // redirect handled by page
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <Card className="w-full max-w-sm">
            <CardHeader className="text-lg font-semibold">Create Account</CardHeader>
            <CardContent className="space-y-4">
                <form onSubmit={handleSignup} className="space-y-4">
                    <Input
                        type="text"
                        placeholder="Name"
                        required
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                    <Input
                        type="email"
                        placeholder="Email"
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />

                    <Input
                        type="password"
                        placeholder="Password (min 6 characters)"
                        minLength={6}
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    {error && (
                        <p className="text-sm text-red-500">{error}</p>
                    )}

                    <Button className="w-full" disabled={loading}>
                        {loading ? "Creating account..." : "Sign Up"}
                    </Button>
                </form>
            </CardContent>
        </Card>

    );
}
