export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div style={{ padding: "20px", background: "#fffaf3", minHeight: "100vh" }}>
      {children}
    </div>
  );
}

