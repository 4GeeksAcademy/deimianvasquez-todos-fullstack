import React, { useContext } from "react";
import { Context } from "../store/appContext";

import "../../styles/home.css";
import Todos from "./Todos.jsx";
import { Navigate } from "react-router-dom";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<>
		{
			store.token ?
			<Todos/> :
			<Navigate to={"/login"}/>
		}
		</>
	);
};
