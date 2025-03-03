import { User } from "@heroui/react";

function ActivitiesPart() {
    interface ActivitiesPartProps {
        id: number;
        activity: string;
        time: Date;
        image: string;
    }

    const data: ActivitiesPartProps[] = [
        {
            id: 1,
            activity: "Opened the email",
            time: new Date(2023, 10, 24, 10, 30),
            image: "https://i.pravatar.cc/150?u=a042581f4e29026024d"
        },
        {
            id: 2,
            activity: "Entered valid data",
            time: new Date(2023, 10, 24, 11, 15),
            image: "https://i.pravatar.cc/150?u=a042581f4e29026704d"
        },
        {
            id: 4,
            activity: "Downloaded a file",
            time: new Date(2023, 10, 22, 14, 45),
            image: "https://i.pravatar.cc/150?u=a048581f4e29026701d"
        },
        {
            id: 5,
            activity: "Opened the email",
            time: new Date(2023, 10, 21, 9, 0),
            image: "https://i.pravatar.cc/150?u=a092581d4ef9026700d"
        }
    ];

    return (
        <div className="flex flex-col items-center ml-4 mt-4 w-full"> {/* Added w-full for full width */}
            {data.map((activity: ActivitiesPartProps) => (
                <div
                    key={activity.id}
                    className="flex mb-2 px-4 py-2 items-center hover:cursor-pointer hover:bg-[#F9F9FA] rounded-lg w-full transition-colors duration-200" /* Added bg-[#F9F9FA], py-2 for padding, rounded-lg, w-full, transition */
                >
                    <User
                        avatarProps={{
                            src: activity.image,
                            radius: "full",
                            size: "sm" // Made avatar size smaller ('sm' for small, adjust as needed)
                        }}
                        name={
                            <p className="text-sm font-medium text-gray-700 group-hover:text-black transition-all duration-200"> {/* Smaller activity text, black on hover */}
                                {activity.activity}
                            </p>
                        }
                        description={
                            <p className="text-xs text-gray-500 group-hover:text-black group-hover:text-sm transition-all duration-200">
                                {activity.time.toLocaleString()}
                            </p>
                        }
                        className="group w-full" 
                    ></User>
                </div>
            ))}
        </div>
    );
}

export default ActivitiesPart;