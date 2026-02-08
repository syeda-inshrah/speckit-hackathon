export default function TestPage() {
  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h1>Test Page</h1>
      <p>If you can see this, the Next.js app is working correctly.</p>
      <p>Current time: {new Date().toISOString()}</p>
      <a href="/">Go to Home</a>
    </div>
  );
}
