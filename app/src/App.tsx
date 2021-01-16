import React from "react";
import "./App.scss";
import "antd/dist/antd.css";
import SurveyPage from "./pages/SurveyPage";

function App() {
  return (
    <div className="App">
      <SurveyPage />
      <div className="footer">
        <a
          href="https://github.com/tobigs-reco-conf-1314/Tobigs-Wine-Reco"
          target="_blank"
          rel="noreferrer"
        >
          Tommelier
        </a>{` ©2021 Created by Tobigs Conference 13-14th`}
      </div>
    </div>
  );
}

export default App;
