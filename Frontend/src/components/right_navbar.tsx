import ActivitiesPart from "@/components/activitiesPart";
function Right_Navbar(){
return(
<div className="flex flex-col w-[300px] items-center border-l border-gray-200 ml-4">
    <h2 className="text-md font-semibold text-black pt-4 pl-4">Activities</h2>
    <ActivitiesPart></ActivitiesPart>
</div>
);
}
export default Right_Navbar

