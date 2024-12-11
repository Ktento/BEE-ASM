import { Box, Button, Heading } from "@yamada-ui/react";
import { useLocation, useNavigate } from "react-router-dom";
import { CVEInfo } from "../types/Restult";
import { useMemo } from "react";
import { Column, Table } from "@yamada-ui/table";

type CVEInfoAndCPE = CVEInfo & {
  cpe: string;
};

export const DetailHost = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const cves = location.state?.cves as { [key: string]: CVEInfo[] };
  const host = location.state?.host as string;
  const cpes = location.state?.cpes as string[];

  const getBackgroundColor = (cvss?: number) => {
    if (cvss === undefined) return "#ffffff"; // デフォルトの白
    if (cvss >= 0.1 && cvss <= 3.9) return "#21b803"; // Low (緑)
    if (cvss >= 4.0 && cvss <= 6.9) return "#fbbc04"; // Medium (黄)
    if (cvss >= 7.0 && cvss <= 8.9) return "#f66e0b"; // High (橙)
    if (cvss >= 9.0 && cvss <= 10.0) return "#f41907"; // Critical (赤)
    return "#ffffff";
  };

  const columns = useMemo<Column<CVEInfoAndCPE>[]>(
    () => [
      {
        header: "CPE",
        accessorKey: "cpe",
      },
      {
        header: "CVE-ID",
        accessorKey: "id",
      },
      {
        header: "CVSS",
        accessorKey: "cvss",
      },
      {
        header: "発行日",
        accessorKey: "Published",
      },
      {
        header: "説明",
        accessorKey: "summary",
      },
    ],
    []
  );

  return (
    <Box as={"main"} p={5}>
      <Box p={5} display={"flex"} justifyContent={"space-between"}>
        <Heading>{host}の結果</Heading>
        <Button colorScheme="purple" onClick={() => navigate(-1)}>
          前のページに戻る
        </Button>
      </Box>

      {cpes.map((cpe) => {
        const targetCve: CVEInfoAndCPE[] = cpes.flatMap((cpe) =>
          (cves[cpe] || []).map((cve) => ({
            ...cve,
            cpe,
          }))
        );

        return (
          <Table
            columns={columns}
            data={targetCve}
            selectColumnProps={false}
            key={cpe}
            headerProps={(header) => {
              const columnHeader = header.column.columnDef.header;
              if (columnHeader === "CVE-ID") {
                return {
                  w: "150px",
                };
              }
              if (columnHeader === "CVSS") {
                return {
                  w: "80px",
                };
              }
              return {};
            }}
            cellProps={({ column, getValue }) => {
              if (
                column.columnDef.header === "CVE-ID" ||
                column.columnDef.header === "CPE"
              ) {
                return {
                  alignContent: "center",
                  textAlign: "center",
                };
              }
              if (column.columnDef.header === "CVSS") {
                return {
                  bg: getBackgroundColor(getValue()),
                  alignContent: "center",
                  textAlign: "center",
                };
              }
              return {};
            }}
          />
        );
      })}
    </Box>
  );
};
