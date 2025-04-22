import { useEffect, useState } from "react";
import DefaultLayout from "@/layouts/default";
import {
	Button,
	Input,
	Select,
	SelectItem,
	Selection,
	Chip,
	Card,
	CardBody,
	Checkbox,
	Divider,
} from "@heroui/react";
import { useNavigate } from "react-router-dom";
import { Campaign, campaignService } from "@/services/campaign.service";
import { Scenario, scenarioService } from "@/services/scenario.service";
import { employeeService } from "@/services/employee.service";
import { toast } from "react-hot-toast";

interface Employee {
	email: string;
	first_name: string;
	last_name: string;
	criticality: string;
	dept_name: string;
}

export default function CreateCampaignPage() {
	const navigate = useNavigate();
	const [loading, setLoading] = useState(false);
	const [scenarios, setScenarios] = useState<Scenario[]>([]);
	const [employees, setEmployees] = useState<Employee[]>([]);
	const [selectedEmployees, setSelectedEmployees] = useState<Set<string>>(new Set());
	const [campaignData, setCampaignData] = useState({
		name: "",
		scenario_id: 0,
	});

	useEffect(() => {
		fetchScenarios();
		fetchEmployees();
	}, []);

	const fetchScenarios = async () => {
		try {
			const response = await scenarioService.getAll();
			setScenarios(response.data.scenarios);
		} catch (error) {
			console.error("Error fetching scenarios:", error);
			toast.error("Failed to load scenarios");
		}
	};

	const fetchEmployees = async () => {
		try {
			const response = await employeeService.getAll();
			setEmployees(response.data.employees);
		} catch (error) {
			console.error("Error fetching employees:", error);
			toast.error("Failed to load employees");
		}
	};

	const handleScenarioChange = (keys: Selection) => {
		if (keys === "all") return;
		const selectedKey = Array.from(keys)[0];
		if (selectedKey) {
			setCampaignData({
				...campaignData,
				scenario_id: parseInt(selectedKey.toString()),
			});
		}
	};

	const handleEmployeeToggle = (email: string) => {
		const newSelected = new Set(selectedEmployees);
		if (newSelected.has(email)) {
			newSelected.delete(email);
		} else {
			newSelected.add(email);
		}
		setSelectedEmployees(newSelected);
	};

	const handleSelectDepartment = (deptName: string) => {
		const deptEmployees = employees
			.filter(emp => emp.dept_name === deptName)
			.map(emp => emp.email);
		const newSelected = new Set(selectedEmployees);
		deptEmployees.forEach(email => newSelected.add(email));
		setSelectedEmployees(newSelected);
	};

	const handleDeselectDepartment = (deptName: string) => {
		const deptEmployees = employees
			.filter(emp => emp.dept_name === deptName)
			.map(emp => emp.email);
		const newSelected = new Set(selectedEmployees);
		deptEmployees.forEach(email => newSelected.delete(email));
		setSelectedEmployees(newSelected);
	};

	const handleCreateCampaign = async () => {
		if (!campaignData.name || !campaignData.scenario_id || selectedEmployees.size === 0) {
			toast.error("Please fill in all required fields");
			return;
		}

		setLoading(true);
		try {
			await campaignService.startCampaign({
				name: campaignData.name,
				scenario_id: campaignData.scenario_id,
				employee_emails: Array.from(selectedEmployees),
			});
			toast.success("Campaign created successfully");
			navigate("/campaigns");
		} catch (error) {
			console.error("Error creating campaign:", error);
			toast.error("Failed to create campaign");
		} finally {
			setLoading(false);
		}
	};

	// Group employees by department
	const departmentGroups = employees.reduce((groups, employee) => {
		const dept = employee.dept_name;
		if (!groups[dept]) {
			groups[dept] = [];
		}
		groups[dept].push(employee);
		return groups;
	}, {} as Record<string, Employee[]>);

	return (
		<DefaultLayout>
			<div className="px-6 py-8">
				<div className="flex justify-between items-center mb-8">
					<h1 className="text-3xl font-semibold text-[#0077B6]">Create Campaign</h1>
					<div className="space-x-2">
						<Button
							color="danger"
							variant="light"
							onPress={() => navigate(-1)}>
							Cancel
						</Button>
						<Button
							color="primary"
							onPress={handleCreateCampaign}
							isLoading={loading}
							isDisabled={!campaignData.name || !campaignData.scenario_id || selectedEmployees.size === 0}>
							Create Campaign
						</Button>
					</div>
				</div>

				<div className="grid grid-cols-12 gap-8">
					{/* Campaign Details */}
					<Card className="col-span-12 lg:col-span-4">
						<CardBody className="space-y-6 p-6">
							<div>
								<h2 className="text-xl font-semibold mb-4">Campaign Details</h2>
								<div className="space-y-4">
									<Input
										label="Campaign Name"
										placeholder="Enter campaign name"
										value={campaignData.name}
										onChange={(e) =>
											setCampaignData({
												...campaignData,
												name: e.target.value,
											})
										}
									/>
									<Select
										label="Select Scenario"
										placeholder="Choose a phishing scenario"
										selectedKeys={
											campaignData.scenario_id
												? [campaignData.scenario_id.toString()]
												: []
										}
										onSelectionChange={handleScenarioChange}>
										{scenarios.map((scenario) => (
											<SelectItem
												key={scenario.id.toString()}
												textValue={scenario.name}>
												<div className="flex flex-col">
													<span>{scenario.name}</span>
													<span className="text-small text-default-500">
														Level {scenario.level}
													</span>
													{scenario.description && (
														<span className="text-tiny text-default-400">
															{scenario.description}
														</span>
													)}
												</div>
											</SelectItem>
										))}
									</Select>
								</div>
							</div>

							<Divider />

							<div>
								<h3 className="text-lg font-semibold mb-2">Selected Employees</h3>
								<p className="text-default-500 mb-2">
									{selectedEmployees.size} employee{selectedEmployees.size !== 1 ? 's' : ''} selected
								</p>
								<div className="flex flex-wrap gap-2">
									{Array.from(selectedEmployees).map(email => {
										const emp = employees.find(e => e.email === email);
										if (!emp) return null;
										return (
											<Chip
												key={email}
												onClose={() => handleEmployeeToggle(email)}
												variant="flat"
												size="sm">
												{emp.first_name} {emp.last_name}
											</Chip>
										);
									})}
								</div>
							</div>
						</CardBody>
					</Card>

					{/* Employee Selection */}
					<div className="col-span-12 lg:col-span-8 space-y-6">
						<h2 className="text-xl font-semibold mb-2">Select Employees</h2>
						{Object.entries(departmentGroups).map(([dept, deptEmployees]) => {
							const deptSelected = deptEmployees.every(emp => selectedEmployees.has(emp.email));
							const someSelected = deptEmployees.some(emp => selectedEmployees.has(emp.email));
							
							return (
								<Card key={dept}>
									<CardBody className="p-6">
										{/* Department Header */}
										<div className="flex items-center justify-between mb-4 p-3 bg-default-50 rounded-lg">
											<div className="flex items-center gap-3">
												<Checkbox
													isSelected={deptSelected}
													isIndeterminate={!deptSelected && someSelected}
													onValueChange={(selected) => {
														if (selected) {
															handleSelectDepartment(dept);
														} else {
															handleDeselectDepartment(dept);
														}
													}}
												/>
												<h3 className="text-lg font-medium">{dept}</h3>
											</div>
											<span className="text-small text-default-500">
												{deptEmployees.length} employee{deptEmployees.length !== 1 ? 's' : ''}
											</span>
										</div>
										{/* Employee List */}
										<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
											{deptEmployees.map((employee) => (
												<div
													key={employee.email}
													className="flex items-start gap-3 p-3 rounded-lg border border-default-200 hover:bg-default-100 transition-colors duration-150 cursor-pointer"
													onClick={() => handleEmployeeToggle(employee.email)}>
													<Checkbox
														isSelected={selectedEmployees.has(employee.email)}
														readOnly
													/>
													<div>
														<div className="font-medium">
															{employee.first_name} {employee.last_name}
														</div>
														<div className="text-small text-default-500">
															{employee.email}
														</div>
														<Chip
															size="sm"
															className="mt-1"
															color={
																employee.criticality === "high" ? "danger" :
																employee.criticality === "medium" ? "warning" : "success"
															}>
															{employee.criticality} risk
														</Chip>
													</div>
												</div>
											))}
										</div>
									</CardBody>
								</Card>
							);
						})}
					</div>
				</div>
			</div>
		</DefaultLayout>
	);
} 