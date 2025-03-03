import Right_Navbar from "@/components/right_navbar";
import Navbar from "@/components/navbar";
import Cards from "@/components/cards";
import LineChart from "@/components/linechart";
import Barchart from "@/components/barchart";
import PieChart from "@/components/piechart";
export default function OverviewPage() {
  return (
    <>
    <div className="flex">
    <Navbar/>
    <div>
    <div className="mt-6 ml-8">
    <h1 className="text-2xl font-bold text-[#0077B6]">Overview</h1> 
        </div>
        <div className=" flex ml-6 mr-6  gap-4">
        <Cards/>
        </div>
        <div>
          <div className="mt-6 ml-8 rounded-2xl bg-[#F9F9FA] px-4 py-4">
          <LineChart/>
          </div>
          <div className="flex">
          <div className="mt-4 mb-4 ml-8  gap-8 w-[400px] h-[240px] rounded-2xl bg-[#F9F9FA] px-4 ">
          <Barchart/>
          </div>
          <div className="mt-4 mb-4 ml-8 flex w-[400px] h-[240px] rounded-2xl bg-[#F9F9FA] px-4 ">
          <PieChart/>
          </div>
          </div>
        </div>
    </div>
      <Right_Navbar/>
    </div>
    </>
  );
}
