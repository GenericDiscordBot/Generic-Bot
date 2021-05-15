import { Box, chakra, Icon, Flex, useColorModeValue } from '@chakra-ui/react';
import Header from "../components/header";
import Head from 'next/head';
import React from 'react';
import {  } from "@chakra-ui/react";

import { IoMdCheckmarkCircle } from "react-icons/io";

export default function home() {
  return (
    <>
      <Head>
        <title>Bot Dashboard</title>
        <meta property="og:title" content="Bot Dashboard" key="title"/>
      </Head>

      <Header/>

      <Flex
        w="full"
        bg="gray.600"
        p={50}
        alignItems="center"
        justifyContent="center">
        <Flex
          maxW="sm"
          w="full"
          mx="auto"
          bg={useColorModeValue("white", "gray.800")}
          shadow="md"
          rounded="lg"
          overflow="hidden">
          <Flex justifyContent="center" alignItems="center" w={12} bg="green.500">
            <Icon as={IoMdCheckmarkCircle} color="white" boxSize={6} />
          </Flex>

          <Box mx={-3} py={2} px={4}>
            <Box mx={3}>
              <chakra.span
                color={useColorModeValue("green.500", "green.400")}
                fontWeight="bold">
                Success
              </chakra.span>
              <chakra.p
                color={useColorModeValue("gray.600", "gray.200")}
                fontSize="sm">
                Deez Nuts!
              </chakra.p>
            </Box>
          </Box>
        </Flex>
      </Flex>
    </>
  )
}
