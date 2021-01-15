import React, { useState, useEffect } from "react";
import SurveyView from "../components/SurveyView";
import WineVeiw from "../components/WineVeiw";
import { Divider } from "antd";
import { RecoDTO } from "../lib/api";

const SurveyPage = () => {
  const [surveyResult, setSurveyResult] = useState<RecoDTO>();

  useEffect(() => {}, []);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
      className="body"
    >
      <SurveyView setSurveyResult={setSurveyResult} />
      <Divider orientation="center">Recommendations</Divider>
      <div
        className="back"
      >
        <WineVeiw surveyResult={surveyResult} />
      </div>
    </div>
  );
};

export default SurveyPage;
