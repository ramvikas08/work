import { GithubScanForm } from "@/components/github-scan-form";

export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <div className="w-full max-w-4xl space-y-4">
        <h1 className="text-3xl font-bold">AI Technical Recruiter</h1>
        <p className="text-slate-400">
          Enter a GitHub URL to generate a Technical Talent Scorecard PDF. Single Scan is $19 or choose Pro at
          $99/month.
        </p>
        <GithubScanForm />
      </div>
    </main>
  );
}
