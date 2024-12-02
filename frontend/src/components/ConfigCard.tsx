import { Card, CardBody } from "@yamada-ui/react";

interface Props {
  content: JSX.Element;
}

function ConfigCard(props: Props) {
  return (
    <Card>
      <CardBody>{props.content}</CardBody>
    </Card>
  );
}

export default ConfigCard;
