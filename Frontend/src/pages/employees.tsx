import { useState, useEffect } from "react";
import DefaultLayout from "@/layouts/default";
import {
	Table,
	TableHeader,
	TableColumn,
	TableBody,
	TableRow,
	TableCell,
	Button,
	Modal,
	ModalContent,
	ModalHeader,
	ModalBody,
	ModalFooter,
	Input,
	Select,
	SelectItem,
	useDisclosure,
	Chip,
	Selection,
} from "@heroui/react";
import { PlusIcon } from "@heroicons/react/24/outline";
import { employeeService } from "../services/employee.service";
import { departmentService } from "../services/department.service";
import axios from "axios";

enum Criticality {
	LOW = "low",
	MEDIUM = "medium",
	HIGH = "high",
}

interface Department {
	name: string;
}

interface Employee {
	email: string;
	first_name: string;
	last_name: string;
	criticality: Criticality;
	dept_name: string;
}

const criticalityOptions = [
	{ key: Criticality.LOW, label: "Low" },
	{ key: Criticality.MEDIUM, label: "Medium" },
	{ key: Criticality.HIGH, label: "High" },
];

export default function EmployeesPage() {
	const {
		isOpen: isEmployeeModalOpen,
		onOpen: onEmployeeModalOpen,
		onClose: onEmployeeModalClose,
	} = useDisclosure();
	const {
		isOpen: isDeptModalOpen,
		onOpen: onDeptModalOpen,
		onClose: onDeptModalClose,
	} = useDisclosure();

	const [employees, setEmployees] = useState<Employee[]>([]);
	const [departments, setDepartments] = useState<Department[]>([]);
	const [newEmployee, setNewEmployee] = useState<Partial<Employee>>({});
	const [newDepartmentName, setNewDepartmentName] = useState<string>("");
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		fetchEmployees();
		fetchDepartments();
	}, []);

	const fetchEmployees = async () => {
		try {
			setError(null);
			const response = await employeeService.getAll();
			setEmployees(response.data.employees);
		} catch (error) {
			console.error("Error fetching employees:", error);
			setError("Failed to load employees.");
		}
	};

	const fetchDepartments = async () => {
		try {
			setError(null);
			const response = await departmentService.getAll();
			const fetchedDepts = response.data.departments;
			setDepartments(fetchedDepts);
		} catch (error) {
			console.error("Error fetching departments:", error);
			setError("Failed to load departments.");
		}
	};

	const handleCreateEmployee = async () => {
		if (
			!newEmployee.email ||
			!newEmployee.first_name ||
			!newEmployee.last_name ||
			!newEmployee.dept_name ||
			!newEmployee.criticality
		) {
			setError("All fields are required.");
			return;
		}

		try {
			setError(null);
			const response = await employeeService.create({
				email: newEmployee.email,
				first_name: newEmployee.first_name,
				last_name: newEmployee.last_name,
				dept_name: newEmployee.dept_name,
				criticality: newEmployee.criticality,
			});

			setEmployees([...employees, response.data.employee]);
			setNewEmployee({});
			onEmployeeModalClose();
		} catch (error: any) {
			console.error("Error creating employee:", error);
			let errorMessage = "Failed to create employee.";
			if (axios.isAxiosError(error) && error.response) {
				const status = error.response.status;
				const responseData = error.response.data;
				if (status === 400) {
					errorMessage = responseData.message || "Validation error.";
					if (responseData.details) {
						const details = Object.entries(responseData.details)
							.map(
								([field, messages]) =>
									`${field}: ${Array.isArray(messages) ? messages.join(", ") : messages}`
							)
							.join("\n");
						errorMessage += `\nDetails:\n${details}`;
					}
				} else if (status === 409) {
					errorMessage = responseData.message || "Employee already exists.";
				} else {
					errorMessage = responseData.message || `Server error (Status: ${status}).`;
				}
			} else if (error instanceof Error) {
				errorMessage = error.message;
			}
			setError(errorMessage);
		}
	};

	const handleCreateDepartment = async () => {
		if (!newDepartmentName.trim()) {
			setError("Department name cannot be empty.");
			return;
		}
		try {
			setError(null);
			const response = await departmentService.create(newDepartmentName);
			setDepartments([...departments, response.data.department]);
			setNewDepartmentName("");
			onDeptModalClose();
		} catch (error: any) {
			console.error("Error creating department:", error);
			let errorMessage = "Failed to create department.";
			if (axios.isAxiosError(error) && error.response) {
				const status = error.response.status;
				const responseData = error.response.data;
				if (status === 400) {
					errorMessage = responseData.message || "Validation error.";
					if (responseData.details) {
						const details = Object.entries(responseData.details)
							.map(
								([field, messages]) =>
									`${field}: ${Array.isArray(messages) ? messages.join(", ") : messages}`
							)
							.join("\n");
						errorMessage += `\nDetails:\n${details}`;
					}
				} else if (status === 409) {
					errorMessage = responseData.message || "Department already exists.";
				} else {
					errorMessage = responseData.message || `Server error (Status: ${status}).`;
				}
			} else if (error instanceof Error) {
				errorMessage = error.message;
			}
			setError(errorMessage);
		}
	};

	const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setNewEmployee({ ...newEmployee, [e.target.name]: e.target.value });
	};

	const handleSelectChange = (name: string) => (keys: Selection) => {
		if (keys === "all") return;
		const selectedKey = Array.from(keys)[0];
		if (selectedKey) {
			setNewEmployee({ ...newEmployee, [name]: selectedKey });
		}
	};

	const getCriticalityColor = (criticality: Criticality) => {
		switch (criticality) {
			case Criticality.LOW:
				return "success";
			case Criticality.MEDIUM:
				return "warning";
			case Criticality.HIGH:
				return "danger";
			default:
				return "default";
		}
	};

	return (
		<DefaultLayout>
			<div className="px-6 py-4">
				<div className="flex justify-between items-center mb-6">
					<h1 className="text-3xl font-semibold text-[#0077B6]">Employees</h1>
					<div className="flex space-x-2">
						<Button
							color="secondary"
							endContent={<PlusIcon className="h-5 w-5" />}
							onPress={onDeptModalOpen}>
							Add Department
						</Button>
						<Button
							color="primary"
							endContent={<PlusIcon className="h-5 w-5" />}
							onPress={onEmployeeModalOpen}>
							Add Employee
						</Button>
					</div>
				</div>

				{error && <p className="text-red-500 mb-4">Error: {error}</p>}

				<Table aria-label="Employee list">
					<TableHeader>
						<TableColumn>EMAIL</TableColumn>
						<TableColumn>FIRST NAME</TableColumn>
						<TableColumn>LAST NAME</TableColumn>
						<TableColumn>DEPARTMENT</TableColumn>
						<TableColumn>CRITICALITY</TableColumn>
					</TableHeader>
					<TableBody items={employees}>
						{(item) => (
							<TableRow key={item.email}>
								<TableCell>{item.email}</TableCell>
								<TableCell>{item.first_name}</TableCell>
								<TableCell>{item.last_name}</TableCell>
								<TableCell>{item.dept_name}</TableCell>
								<TableCell>
									<Chip
										color={getCriticalityColor(item.criticality)}
										variant="flat">
										{item.criticality.toUpperCase()}
									</Chip>
								</TableCell>
							</TableRow>
						)}
					</TableBody>
				</Table>

				<Modal
					isOpen={isEmployeeModalOpen}
					onClose={() => {
						onEmployeeModalClose();
						setError(null);
					}}
					isDismissable={false}
					hideCloseButton={true}>
					<ModalContent>
						<ModalHeader>Add New Employee</ModalHeader>
						<ModalBody>
							{error && <p className="text-red-500 text-sm">Error: {error}</p>}
							<div className="space-y-4">
								<Input
									label="Email"
									name="email"
									placeholder="Enter employee email"
									value={newEmployee.email || ""}
									onChange={handleInputChange}
									isRequired
								/>
								<Input
									label="First Name"
									name="first_name"
									placeholder="Enter first name"
									value={newEmployee.first_name || ""}
									onChange={handleInputChange}
									isRequired
								/>
								<Input
									label="Last Name"
									name="last_name"
									placeholder="Enter last name"
									value={newEmployee.last_name || ""}
									onChange={handleInputChange}
									isRequired
								/>
								<Select
									label="Department"
									placeholder="Select department"
									selectedKeys={
										newEmployee.dept_name ? [newEmployee.dept_name] : []
									}
									onSelectionChange={handleSelectChange("dept_name")}
									isRequired>
									{departments.map((dept) =>{
										console.log(dept);
										return (
										<SelectItem key={dept.name} textValue={dept.name}>
											{dept.name}
										</SelectItem>
									) }
									)}
								</Select>
								<Select
									label="Criticality"
									placeholder="Select criticality level"
									selectedKeys={
										newEmployee.criticality ? [newEmployee.criticality] : []
									}
									onSelectionChange={handleSelectChange("criticality")}
									isRequired>
									{criticalityOptions.map((option) => (
										<SelectItem key={option.key} textValue={option.label}>
											{option.label}
										</SelectItem>
									))}
								</Select>
							</div>
						</ModalBody>
						<ModalFooter>
							<Button
								color="danger"
								variant="light"
								onPress={() => {
									onEmployeeModalClose();
									setError(null);
								}}>
								Cancel
							</Button>
							<Button color="primary" onPress={handleCreateEmployee}>
								Add Employee
							</Button>
						</ModalFooter>
					</ModalContent>
				</Modal>

				<Modal
					isOpen={isDeptModalOpen}
					onClose={() => {
						onDeptModalClose();
						setError(null);
					}}
					isDismissable={false}
					hideCloseButton={true}>
					<ModalContent>
						<ModalHeader>Add New Department</ModalHeader>
						<ModalBody>
							{error && <p className="text-red-500 text-sm">Error: {error}</p>}
							<Input
								label="Department Name"
								placeholder="Enter new department name"
								value={newDepartmentName}
								onChange={(e) => setNewDepartmentName(e.target.value)}
								isRequired
							/>
						</ModalBody>
						<ModalFooter>
							<Button
								color="danger"
								variant="light"
								onPress={() => {
									onDeptModalClose();
									setError(null);
								}}>
								Cancel
							</Button>
							<Button color="primary" onPress={handleCreateDepartment}>
								Create Department
							</Button>
						</ModalFooter>
					</ModalContent>
				</Modal>
			</div>
		</DefaultLayout>
	);
}
