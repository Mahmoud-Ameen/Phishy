import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router";
import { TbLogout2 } from "react-icons/tb";
import { RiPieChartLine } from "react-icons/ri";
import { MdOutlineCampaign } from "react-icons/md";
import { Avatar } from "@heroui/react";
import admin from "../assets/admin.jpg";

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [selected, setSelected] = useState("Dashboard");
  const [tubePosition, setTubePosition] = useState(0);

  // Synchronize the selected menu with the current URL path
  useEffect(() => {
    switch (location.pathname) {
      case "/overview":
        setSelected("Overview");
        setTubePosition(-4);
        break;
      case "/campaigns":
        setSelected("Campaigns");
        setTubePosition(65);
        break;
      default:
        setSelected("Overview");
        setTubePosition(-4);
    }
  }, [location.pathname]);

  return (
    <>
    <div className="flex flex-col items-center w-52 h-screen bg-white text-white pt-4 relative border-r border-gray-200">
      {/* Admin Section */}
      <div className="flex items-center mb-4 ml-[-10px]">
        <Avatar isBordered size="md" src={admin} />
        <h2 className="text-md font-medium text-black ml-2">Admin</h2>
      </div>
      {/* Menu Items */}
      <div className="grid grid-cols-1 gap-8 mt-16 relative ml-[1px]">
        {/* Tube */}
        <div
          className="absolute left-[-54px] h-10 w-2 bg-[#023E8A] rounded-full transition-transform transition-all ease-in-out duration-300"
          style={{
            transform: `translateY(${tubePosition}px)`,
          }}
        ></div>

        {/* Overview Menu Item */}
        <div>
          <button
            className="flex items-center mb-4"
            onClick={() => {
              if (selected !== "Overview") {
                setSelected("Overview");
                navigate("/overview");
              }
            }}
          >
            <RiPieChartLine className="text-[#023E8A] text-2xl mr-2"></RiPieChartLine>
            <h1 className="text-sm font-normal text-[#023E8A]">Overview</h1>
          </button>
        </div>

        {/* Campaigns Menu Item */}
        <div>
          <button
            className="flex items-center"
            onClick={() => {
              if (selected !== "Campaigns") {
                setSelected("Campaigns");
                navigate("/campaigns");
              }
            }}
          >
            <MdOutlineCampaign className="text-[#023E8A] text-2xl mr-2"></MdOutlineCampaign>
            <h1 className="text-sm font-normal text-[#023E8A]">Campaigns</h1>
          </button>
        </div>
      </div>

      {/* Log Out Section */}
      <div className="absolute bottom-4 w-full px-4">
        <button onClick={() => navigate("/")} className="flex items-center">
          <TbLogout2 className="text-[#023E8A] text-2xl mr-2"></TbLogout2>
          <h1 className="text-sm font-normal text-[#023E8A]">Log out</h1>
        </button>
      </div>
    </div>
    </>
  );
}

export default Navbar;