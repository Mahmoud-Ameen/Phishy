import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router";
import { TbLogout2 } from "react-icons/tb";
import { RiPieChartLine } from "react-icons/ri";
import { MdOutlineCampaign } from "react-icons/md";
import { BsClipboardCheck } from "react-icons/bs";
import { FiUsers } from "react-icons/fi";
import { GlobeAltIcon } from "@heroicons/react/24/outline";
import { Avatar } from "@heroui/react";
import admin from "../assets/admin.jpg";

function Navbar() {
	const navigate = useNavigate();
	const location = useLocation();
	const [selected, setSelected] = useState("Dashboard");
	const [tubePosition, setTubePosition] = useState(0);

	// Synchronize the selected menu with the current URL path
	useEffect(() => {
		// Calculate position based on index to make it more maintainable
		const items = ["/overview", "/campaigns", "/scenarios", "/employees", "/admin/domains"];
		const itemHeight = 56; // Approximate height including gap (adjust as needed)
		const initialOffset = -4; // Initial offset for the first item

		const index = items.findIndex(path => location.pathname.startsWith(path));
		
		if (index !== -1) {
			const itemName = location.pathname.split('/')[1]; // Get base name (e.g., 'overview', 'admin')
			let selectedName = itemName.charAt(0).toUpperCase() + itemName.slice(1);
			if(itemName === 'admin') selectedName = 'Domains'; // Specific case for admin/domains

			setSelected(selectedName); 
			setTubePosition(initialOffset + index * itemHeight);
		} else {
			// Default case if path doesn't match known items
			setSelected("Overview");
			setTubePosition(initialOffset);
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
				<div className="grid grid-cols-1 gap-6 mt-16 relative ml-[1px]">
					{/* Tube */}
					<div
						className="absolute left-[-54px] h-10 w-2 bg-[#023E8A] rounded-full transition-transform transition-all ease-in-out duration-300"
						style={{
							transform: `translateY(${tubePosition}px)`,
						}}></div>

					{/* Overview Menu Item */}
					<div>
						<button
							className="flex items-center mb-4"
							onClick={() => {
								if (selected !== "Overview") {
									setSelected("Overview");
									navigate("/overview");
								}
							}}>
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
							}}>
							<MdOutlineCampaign className="text-[#023E8A] text-2xl mr-2"></MdOutlineCampaign>
							<h1 className="text-sm font-normal text-[#023E8A]">Campaigns</h1>
						</button>
					</div>

					{/* Scenarios Menu Item */}
					<div>
						<button
							className="flex items-center"
							onClick={() => {
								if (selected !== "Scenarios") {
									setSelected("Scenarios");
									navigate("/scenarios");
								}
							}}>
							<BsClipboardCheck className="text-[#023E8A] text-2xl mr-2"></BsClipboardCheck>
							<h1 className="text-sm font-normal text-[#023E8A]">Scenarios</h1>
						</button>
					</div>

					{/* Employees Menu Item */}
					<div>
						<button
							className="flex items-center"
							onClick={() => {
								if (selected !== "Employees") {
									setSelected("Employees");
									navigate("/employees");
								}
							}}>
							<FiUsers className="text-[#023E8A] text-2xl mr-2"></FiUsers>
							<h1 className="text-sm font-normal text-[#023E8A]">Employees</h1>
						</button>
					</div>

					{/* Domains Menu Item (New) */}
					<div>
						<button
							className="flex items-center"
							onClick={() => {
								if (selected !== "Domains") {
									setSelected("Domains");
									navigate("/admin/domains");
								}
							}}>
							<GlobeAltIcon className="text-[#023E8A] text-2xl mr-2"></GlobeAltIcon>
							<h1 className="text-sm font-normal text-[#023E8A]">Domains</h1>
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
