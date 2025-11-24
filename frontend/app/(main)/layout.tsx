import HeaderSelect from "@/components/main/select-main/HeaderSelect";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      {children}
    </>
  );
}