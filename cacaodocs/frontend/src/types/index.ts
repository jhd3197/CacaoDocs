// This file exports any TypeScript types or interfaces used throughout the application.

export interface PageProps {
    title: string;
    content: React.ReactNode;
}

export interface SidebarItem {
    label: string;
    path: string;
}