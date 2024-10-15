import { writable } from 'svelte/store';

export function createPasswordDialog() {
	let showModal = writable(false);
	let password = writable('');
	let loading = writable(false);
	let valid = writable(false);
	let wrongPassword = writable<string | undefined>(undefined);

	async function getPassword(email: string, apiEndpoint: string, enteredPassword: string) {
		loading.set(true);

		try {
			const response = await fetch(apiEndpoint, {
				method: 'POST',
				body: JSON.stringify({ email, password: enteredPassword }),
				headers: {
					'Content-Type': 'application/json'
				}
			});

			const data = await response.json();

			loading.set(false);

			if (data.status === 200) {
				password.set(data.password);
				valid.set(true);
				showModal.set(false);
			} else if (data.status === 401) {
				wrongPassword.set(data.response);
				valid.set(false);
			}
		} catch (error) {
			console.error('Could not verify the password');
		}
	}

	return {
		showModal,
		password,
		loading,
		valid,
		wrongPassword,
		getPassword
	};
}
