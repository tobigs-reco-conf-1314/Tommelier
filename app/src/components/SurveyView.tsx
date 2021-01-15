import React from "react";
import * as Survey from "survey-react";

Survey.StylesManager.applyTheme("modern");

interface Props {
  setSurveyResult: any;
}

const SurveyView = ({ setSurveyResult }: Props) => {
  const json = {
    title: "🍇 Tommelier: 초심자를 위한 와인 취향 질문 🍷",
    pages: [
      {
        title: "어떤 분위기에서 마시나요?",
        questions: [
          {
            type: "radiogroup",
            name: "mood",
            title: "이 중에서 하나 선택해주세요.",
            isRequired: true,
            choices: [
              "음식과 함께",
              "가볍게 즐기기 좋은",
              "달콤한 분위기",
              "디저트와 함께",
              "파티 분위기",
              "취하고 싶을 때",
            ],
          },
        ],
      },
      {
        title: "어떤 음식을 함께 같이 드시나요?",
        questions: [
          {
            type: "radiogroup",
            name: "food",
            title: "이 중에서 하나 선택해주세요.",
            colCount: 4,
            isRequired: true,
            choices: [
              "닭고기",
              "돼지고기",
              "소고기",
              "양고기",
              "연어/참치",
              "조개",
              "흰살생선",
              "매운 음식",
              "파스타",
              "버섯",
              "채소",
              "식전주",
              "에피타이저",
              "단 디저트",
              "과일 디저트",
              "부드러운 치즈",
              "딱딱한 치즈",
              "블루치즈",
            ],
          },
        ],
      },
      {
        title: "각 맛에 대한 선호도를 선택해주세요.",
        questions: [
          {
            type: "rating",
            name: "sweet",
            title: "당도는 어느정도로 선호하시나요",
            isRequired: true,
            minRateDescription: "매우 선호하지 않음",
            maxRateDescription: "매우 선호함",
          },
          {
            type: "rating",
            name: "tannin",
            title: "떫은 맛(타닌)은 어느정도로 선호하시나요",
            isRequired: true,
            minRateDescription: "매우 선호하지 않음",
            maxRateDescription: "매우 선호함",
          },
          {
            type: "rating",
            name: "body",
            title:  "바디감은 어느정도로 선호하시나요",
            isRequired: true,
            minRateDescription: "매우 선호하지 않음",
            maxRateDescription: "매우 선호함",
          },
          {
            type: "rating",
            name: "acidity",
            title:  "산도는 어느정도로 선호하시나요",
            isRequired: true,
            minRateDescription: "매우 선호하지 않음",
            maxRateDescription: "매우 선호함",
          },
        ],
      },
    ],
  };
  const survey = new Survey.Model(json);
  survey.locale = "ko";

  return (
    <Survey.Survey
      model={survey}
      onComplete={(result: any) => {
        setSurveyResult(result.data);
      }}
    />
  );
};

export default SurveyView;
