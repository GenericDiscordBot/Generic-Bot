import { ChakraProvider } from '@chakra-ui/react';
import { AppProps } from 'next/app';
import Head from 'next/head';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <meta content="bot dashboard yes" name="description"/>
        <meta charSet="utf-8"/>
        <meta content="width=device-width, initial-scale=1" name="viewport"/>
      </Head>
      <ChakraProvider>
        <Component {...pageProps} />
      </ChakraProvider>
    </>
  );
}
