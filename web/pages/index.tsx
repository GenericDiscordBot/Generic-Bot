import {
    Box,
    Button,
} from '@chakra-ui/react';
import Header from "../components/header";
import Head from 'next/head';
import React from 'react';

export default function home() {
  return (
    <>
      <Head>
        <title>Bot Dashboard</title>
        <meta property="og:title" content="Bot Dashboard" key="title"/>
      </Head>

      <Header/>

      <Box>
        <Button>
          <p>AAAAAAA</p>
        </Button>
      </Box>
    </>
  )
}
