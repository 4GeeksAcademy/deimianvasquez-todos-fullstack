const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			token: localStorage.getItem("token") || null,
			currentUser: localStorage.getItem("currentUser") || null
		},
		actions: {
			register: async (user) => {
				try {
					const response = await fetch(`${process.env.BACKEND_URL}/register`, {
						method: "POST",
						body: user
					})

					return response.status

				} catch (error) {
					console.log(error)
					return response.status
				}
			},
			login: async (user) => {
				try {
					const response = await fetch(`${process.env.BACKEND_URL}/login`, {
						method: "POST",
						headers: {
							"Content-Type": "application/json"
						},
						body: JSON.stringify(user)
					})
					const data = await response.json()
					if (response.ok) {
						setStore({
							token: data.token,
							currenUser: data.current_user
						})

						localStorage.setItem("token", data.token)
						localStorage.setItem("currentUser", JSON.stringify(data.current_user))

					}
					return response.status

				} catch (error) {
					console.log(error)
					return false
				}
			},
			logout: () => {
				// # a la api donde en la db se guardan los token muertos
				setStore({
					token: null,
					currenUser: null
				})
				localStorage.removeItem("token")
				localStorage.removeItem("currentUser")
			}
		}
	};
};

export default getState;
