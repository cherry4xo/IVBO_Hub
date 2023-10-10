import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Provider } from "@/redux/provider";
import { ChakraProvider } from "@chakra-ui/react";
import { Launcher } from "@/components/Common";
import Script from "next/script";

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'Create Next App',
    description: 'Generated by create next app',
}

export default function RootLayout({ children, }: { children: React.ReactNode }) {
    return <html lang='en'>
    <body className={inter.className}>
    <Provider>
        <ChakraProvider>
            <Launcher />
            <Script src="https://telegram.org/js/telegram-web-app.js" />
            {children}
        </ChakraProvider>
    </Provider>
    </body>
    </html>
}
