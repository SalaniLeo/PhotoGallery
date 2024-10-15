<script lang="ts">
	import { rootData, throwError } from '$lib/stores';

	let dialog: HTMLDialogElement;

	export let { valid, showModal, password, loading, errormessage } = createValues();

	function createValues() {
		let valid = false;
		let showModal: boolean = true;
		let password: string;
		let loading: boolean = false;
		let errormessage: string | undefined = undefined;
		return { valid, showModal, password, loading, errormessage };
	}

	$: if (showModal && dialog) {
		dialog.showModal();
	} else if (!showModal && dialog) {
		dialog.close();
	}

	async function getPassword() {
		loading = true;
		let email = $rootData.user.info.email;
		try {
			const response = await fetch($rootData.addresses.check_password, {
				method: 'POST',
				body: JSON.stringify({ email, password }),
				headers: {
					'Content-Type': 'application/json',
					'x-api-key': $rootData.apikey
				}
			});
			const data = await response.json();
			loading = false;
			if (data.status === 200) {
				password = data.password;
				valid = true;
				dialog.close();
			} else if (data.status === 401) {
				valid = false;
				//@ts-ignore
				errormessage = 'Wrong password';
			}
		} catch (error) {
			throwError.set('Something went wrong, try again');
		}
	}
</script>

<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<dialog
	bind:this={dialog}
	on:close={() => (showModal = false)}
	on:click|self={() => {
		dialog.close();
		valid = false;
		password = '';
	}}
	class="outline"
>
	<div class="dialog-content" on:click|stopPropagation>
		<h2>Verify password:</h2>
		<input
			type="password"
			name="password"
			id="password"
			class:inputerror={errormessage}
			bind:value={password}
			on:keydown={(e) => {
				if (errormessage != undefined) {
					errormessage = undefined;
				}
				if (e.key == 'Enter') {
					getPassword();
				}
			}}
		/>
	</div>
	{#if errormessage != undefined}
		<small class="errorfont">{errormessage}</small>
	{/if}
	<div class="buttons">
		<button
			on:click={() => {
				getPassword();
			}}
		>
			Confirm
		</button>
		<button on:click={() => dialog.close()}> Cancel </button>
	</div>
</dialog>

<style>
	.inputerror {
		border-bottom: 2px solid var(--font-error-color);
	}
	.dialog-content {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin: 0.5rem;
	}
	.buttons {
		display: flex;
		margin: 0.5rem;
		margin-top: 1rem;
		justify-content: end;
		gap: 0.5rem;
	}
	h2 {
		margin: 0.5rem;
	}
	dialog {
		background-color: var(--primary-color);
		border-radius: var(--border-radius-heavy);
		border: none;
		padding: 0.5rem;
		width: 16rem;
		min-width: fit-content;
		height: fit-content;
		outline: 2px solid var(--accent-color-primary);
	}
	dialog::backdrop {
		background: rgba(0, 0, 0, 0.3);
		backdrop-filter: blur(4px);
	}
	dialog[open] {
		animation: zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
	}
	@keyframes zoom {
		from {
			transform: scale(0.95);
		}
		to {
			transform: scale(1);
		}
	}
	dialog[open]::backdrop {
		animation: fade 0.2s ease-out;
	}
	@keyframes fade {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
</style>
