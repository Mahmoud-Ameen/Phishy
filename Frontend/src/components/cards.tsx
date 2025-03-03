import {Card, CardHeader} from "@heroui/react";
import { FaArrowTrendUp, FaArrowTrendDown,FaEquals } from "react-icons/fa6";

interface CardData {
  title: string;
  number: number;
  percentage: number;
}

export default function App() {
  const cardData: CardData[] = [
    {
      title: "Clicked the Link",
      number: 7265,
      percentage: 11.01,
    },
    {
      title: "Opened the Email",
      number: 3671,
      percentage: -0.03,
    },
    {
      title: "Downloaded a File",
      number: 156,
      percentage:15.03
    },
    {
      title: "Entered Data",
      number: 2318,
      percentage: 3.18
    },
  ];

  return (
    <div className="flex mt-2 gap-4">
      {cardData.map((card, index) => (
        <Card key={index} className={`py-4 w-[180px] h-[90px]`} style={index %2 == 0 ? {backgroundColor:"#7AADD4" } : {backgroundColor:"#d2e4f7" }}>
          <CardHeader className="pb-0 pt-2 px-4 flex-col items-start">
            <p className="text-xs font-light text-black-200 ">{card.title}</p>
            <div className="flex motion-opacity-in-0 motion-translate-y-in-100">
              <h4 className="font-bold text-xl pt-2 text-black pl-2 ">{card.number.toLocaleString()}</h4> 
              <div className="flex pt-4 pl-6">
                <p className="text-xs text-black">
                  {card.percentage.toFixed(2)}% 
                </p>
                {card.percentage > 0 ? (
                  <FaArrowTrendUp className="text-xl pl-1 pb-1 text-green-800"/> 
                ) :card.percentage<0 ? (
                  <FaArrowTrendDown className="text-xl pl-1 pb-1 text-red-500"/>  
                ):(
                  <FaEquals className="text-xl pl-1 pb-1 text-black"/>
                )}
              </div>
            </div>
          </CardHeader>
        </Card>
      ))}
    </div>
  );
}