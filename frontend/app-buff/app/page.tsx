
import Tiktok from "@/components/TiktokSidebar"
import Head from 'next/head';

export default function Home() {
  return (
    <main>

      <Head>
        <title>HCM57 App BUFF TikTok</title>
        <meta name="description" content="App buff tiktok" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      {/* <Hero/> */}
      {/* <RouterPage/> */}
      <Tiktok />
    </main>
  );
}
