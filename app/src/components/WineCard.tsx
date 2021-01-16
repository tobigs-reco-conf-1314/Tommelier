import React from "react";
import { WineDTO } from "../lib/api";
import "./WineCard.scss";

const TYPEID2WINETYPE: Record<number, string> = {
  1: "Red",
  2: "White",
  3: "Sparkling",
  4: "Rose",
  7: "Dessert",
  24: "Fortified",
};

interface Props {
  wine: WineDTO;
}

const WineCard = ({ wine }: Props) => {
  return (
    <div className="card card--dark">
      <div className="card__image-container">
        <img
          onError={(e: any) => {
            e.target.onerror = null;
            e.target.src =
              "http://storage.googleapis.com/tommelier/imgs/1525655.png";
          }}
          src={wine.img_url}
          alt="Eevee"
          className="card__image"
        />
      </div>

      <figcaption className="card__caption">
        <h1 className="card__name">{wine.name}</h1>

        <h3 className="card__type">{TYPEID2WINETYPE[wine.wine_type]}</h3>

        <table className="card__stats">
          <tbody>
            <tr>
              <th>Avg. Rating</th>
              <td>{wine.rating_average}</td>
            </tr>
            <tr>
              <th>Acidity</th>
              <td>{wine.acidity?.toFixed(1)}</td>
            </tr>

            <tr>
              <th>Body</th>
              <td>{wine.body?.toFixed(1)}</td>
            </tr>

            <tr>
              <th>Sweetness</th>
              <td>{wine.sweetness?.toFixed(2)}</td>
            </tr>
            <tr>
              <th>Tannin</th>
              <td>{wine.tannin?.toFixed(2)}</td>
            </tr>
            <tr>
              <th>Rank in Country</th>
              <td>{wine.rank_country}</td>
            </tr>
          </tbody>
        </table>

        <div className="card__abilities">
          <h4 className="card__ability">
            <span className="card__label">Grape</span>
            {wine.grapes[0]}
          </h4>
          <h4 className="card__ability">
            <span className="card__label">Foods</span>
            {wine.foods.join(", ")}
          </h4>
        </div>
      </figcaption>
    </div>
  );
};

export default WineCard;
