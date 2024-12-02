import { Box, Button, FormControl, Heading, Input } from "@yamada-ui/react";
import { useState } from "react";
import Config from "../components/Config";

function Index() {
  const [domain, setDomain] = useState("");

  const handleSubmit = async (e: React.ChangeEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/run-asm");
      console.log(res);
    } catch (error) {
      console.error("Error calling backend:", error);
    }
    console.log(domain);
  };

  return (
    <Box as={"main"} p={5}>
      <Heading>ASM Tool</Heading>
      <Box as={"div"} p={5}>
        <form onSubmit={handleSubmit}>
          <FormControl label="対象ドメイン" py={5}>
            <Input
              placeholder="domain"
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              width={"70%"}
            />
          </FormControl>
          <Config />

          <Box display={"flex"} justifyContent={"end"}>
            <Button type="submit" colorScheme="purple" variant="outline">
              実行
            </Button>
          </Box>
        </form>
      </Box>
    </Box>
  );
}

export default Index;
