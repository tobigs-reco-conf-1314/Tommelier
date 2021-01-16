import React, { useEffect, useState } from "react";
import api, { WineDTO, RecoDTO } from "../lib/api";
import WineCard from "../components/WineCard";
import { Row, Col } from "antd";

interface Props {
  surveyResult: RecoDTO | undefined;
}

const WineVeiw = ({ surveyResult }: Props) => {
  const [wines, setWines] = useState<WineDTO[]>([]);

  useEffect(() => {
    const getWineData = async () => {
      if (!surveyResult) {
        return;
      }
      const input = surveyResult;
      const recommendations = await api.getRecommendation(input);
      const wines = await api.getMultiWineInfos(recommendations);
      setWines(wines);
    };

    getWineData();
  }, [surveyResult]);

  return (
    <Row justify="space-around" gutter={{ xs: 8, sm: 16, md: 24, lg: 32 }}>
      {wines?.map((wine) => (
        <Col xs={24} sm={12} md={12} lg={8} xl={6}>
          <WineCard wine={wine} />
        </Col>
      ))}
    </Row>
  );
};

export default WineVeiw;
