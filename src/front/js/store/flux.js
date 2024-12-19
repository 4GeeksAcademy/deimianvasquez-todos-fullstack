const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			token: localStorage.getItem("token") || null,
			currentUser: JSON.parse(localStorage.getItem("currentUser")) || null
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
			},
			resetPassword: async (email) => {
				try {
					const response = await fetch(`${process.env.BACKEND_URL}/reset-password`, {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
							// "Authorization": `Bearer ${getStore().token}` en caso de enviar el token esta es la manera
						},
						body: JSON.stringify(email)
					})

					console.log(response)

				} catch (error) {
					console.log(error)
				}
			},
			updatePassword: async (tokenUpdate, password) => {
				try {
					const response = await fetch(`${process.env.BACKEND_URL}/update-password`, {
						method: "PUT",
						headers: {
							"Authorization": `Bearer ${tokenUpdate}`,
							"Content-Type": "application/json"
						},
						body: JSON.stringify(password)
					})
					console.log(response)
				} catch (error) {
					console.log(error)
				}
			}
		}
	};
};

export default getState;
