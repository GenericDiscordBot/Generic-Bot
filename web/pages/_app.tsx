import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import { AppProps } from 'next/app';
import Head from 'next/head';

export default function App({ Component, pageProps }: AppProps) {
  const colors = {
    brand: {
      900: "#1a365d",
      800: "#153e75",
      700: "#2a69ac",
    },
  }

  const theme = extendTheme({ colors })

  return (
    <>
      <Head>
        <meta content="bot dashboard yes" name="description"/>
        <meta charSet="utf-8"/>
        <meta content="width=device-width, initial-scale=1" name="viewport"/>
      </Head>
      <ChakraProvider theme={theme}>
        <Component {...pageProps} />
      </ChakraProvider>
    </>
  );
}
