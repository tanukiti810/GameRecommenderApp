export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div style={{
      padding: "20px",
      height: "100vh",
      boxSizing: "border-box",
      overflow: "hidden"
    }}>
      {children}
    </div>
  );
}