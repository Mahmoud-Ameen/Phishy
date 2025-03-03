import { useState } from "react";
import { Input, Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button } from "@heroui/react";
import log from "../assets/logo.png";
import { useNavigate } from "react-router-dom";
const LoginPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoginFailedModalVisible, setLoginFailedModalVisible] = useState(false);

  const handleLogin = () => {
    const validEmail = "admin@gmail.com";
    const validPassword = "Admin123";

    if (email === validEmail && password === validPassword) {
      // Redirect to dashboard on successful login
      navigate("/overview");
    } else {
      // Show login failed modal
      setLoginFailedModalVisible(true);
    }
  };

  const closeLoginFailedModal = () => {
    setLoginFailedModalVisible(false);
  };


  return (
    <div className="relative flex justify-center items-center h-screen opacity-95 bg-gradient-to-l from-[#03045E] via-[#0077B6] to-[#CAF0F8]">
      {/* IMAGE PART */}
      <div className="absolute top-[30%] left-[12%] z-30 bg-[#C1E8FF] rounded-2xl py-20 px-10">
        <img
          className="rounded-2xl w-[300px] ml-[0px]"
          src={log}
          alt="logo"
        />
      </div>
      {/* LOGIN FORM */}
      <div className="flex justify-center items-center h-screen w-[560px] mr-[10px]">
        <div className="flex justify-center items-center flex-wrap md:flex-nowrap gap-8 w-full max-w-2xl p-8 rounded-2xl shadow-lg bg-gradient-to-b from-white/70 to-white/40 backdrop-blur-2xl border border-white/50 relative">
          <div className="w-full md:w-1/2 flex flex-col gap-4">
            <div className="flex justify-center items-center">
              <h2 className="text-[26px] mr-4 font-[800] text-gray-800 mb-4">
                Login
              </h2>
            </div>
            <Input
              label="Email"
              type="email"
              onChange={(e) => setEmail(e.target.value)}
              variant="underlined"
              required
            />
            <Input
              label="Password"
              type="password"
              variant="underlined"
              required
              onChange={(e) => setPassword(e.target.value)}
            />
            <button
              onClick={handleLogin}
              className="bg-gradient-to-b from-[#0077B6] to-[#03045E] hover:opacity-80 transition-opacity duration-300 text-white font-bold py-2 px-4 rounded-[45px]"
            >
              Login
            </button>
            <div className="flex justify-end text-center mt-4">
              <a
                href="#"
                className="text-gray-700 text-bold hover:underline delay-75"
              >
                Forgot Password?
              </a>
            </div>
          </div>
        </div>
      </div>
      <Modal hideCloseButton={true} isOpen={isLoginFailedModalVisible} onClose={closeLoginFailedModal}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">
                Invalid Credentials
              </ModalHeader>
              <ModalBody>
                <p className="text-red-500">
                  The email or password you entered is incorrect. Please try
                  again.
                </p>
              </ModalBody>
              <ModalFooter>
                <Button color="danger" variant="light" onPress={onClose}>
                  Close
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </div>
  );
};

export default LoginPage;