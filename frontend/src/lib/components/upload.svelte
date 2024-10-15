<script lang="ts">
	import { showToast } from '$lib';
	import { showCreatePost, rootData } from '$lib/stores';

	export let data;
	const addresses = data['addresses'];

	let input: any;
	let image: any;
	let container;
	let showImage = false;
	let uploading = false;
	let showModal = false;
	let dialog: HTMLDialogElement;
	let title: string, description: string;
	const upload_address = addresses['upload'];

	$: showCreatePost.subscribe((value) => {
		showModal = value;
		if (dialog) {
			value ? dialog.showModal() : dialog.close();
		}
	});

	function onChange() {
		const file = input.files[0];

		if (file) {
			showImage = true;

			const reader = new FileReader();
			reader.addEventListener('load', function () {
				image.setAttribute('src', reader.result);
			});
			reader.readAsDataURL(file);

			return;
		}
		showImage = false;
	}

	async function handleUpload() {
		if (uploading) return;

		uploading = true;
		const file = input?.files?.[0];

		if (!file) {
			alert('Please select a file first.');
			uploading = false;
			return;
		}

		const formData = new FormData();
		formData.append('file', file);
		formData.append('title', title);
		formData.append('description', description);

		try {
			const response = await fetch(upload_address, {
				method: 'POST',
				headers: {
					'x-api-key': $rootData.apikey
				},
				body: formData
			});

			if (!response.ok) {
				throw new Error(`Upload failed: ${response.statusText}`);
			}

			const data = await response.json();
			const { postData } = data;

			showToast('Post uploaded succesfully', data.status);

			$rootData.posts.unshift({
				name: title,
				description: description,
				source: postData.filename,
				id: postData.post_id,
				reactions: [],
				expand_picker: false,
				like_count: 0
			});

			showCreatePost.set(false);
		} catch (error) {
			showToast('Could not upload post: ' + error, 400);
			console.error('Error uploading the file:', error);
		} finally {
			uploading = false;
		}
	}
</script>

<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
<dialog
	bind:this={dialog}
	on:close={() => showCreatePost.set(false)}
	on:click|self={() => dialog.close()}
	class="outline"
>
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div class="dialog-content" on:click|stopPropagation>
		<div class="top">
			<h1>Create new post</h1>
		</div>
		<hr />
		<div class="center">
			<div class="name">
				<label class="text" for="title">Title:</label>
				<input class="textInput" name="title" type="text" bind:value={title} />
			</div>

			<div class="description">
				<label for="description">Description:</label>
				<input class="textInput" name="description" type="text" bind:value={description} />
			</div>

			<div class="file">
				<input bind:this={input} on:change={onChange} type="file" />
				<div bind:this={container}>
					{#if showImage}
						<img bind:this={image} src="" alt="Preview" />
					{/if}
				</div>
			</div>
		</div>
		<hr />
		<div class="bottom">
			<button on:click={handleUpload}> Upload </button>
			<button on:click={() => dialog.close()}> Cancel </button>
		</div>
	</div>
</dialog>

<style>
	dialog {
		background-color: var(--terthiary-color);
		border-radius: var(--border-radius-heavy);
		border: none;
		padding: 0;
		width: max-content;
		height: fit-content;
		border: 2px solid var(--border-color);
		backdrop-filter: blur(--background-blur-heavy);
	}
	dialog::backdrop {
		background: rgba(0, 0, 0, 0.3);
		backdrop-filter: blur(4px);
	}
	.dialog-content {
		padding: 1rem;
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
	.bottom {
		display: flex;
		gap: 0.5rem;
		justify-content: flex-end;
	}
	.center {
		text-align: center;
	}
	button {
		padding: 10px;
		border-radius: var(--border-radius-medium);
	}
	img {
		max-width: 500px;
		max-height: 500px;
	}
	.name,
	dialog .description {
		display: flex;
		gap: 40px;
		width: 400px;
		margin-bottom: 0.25rem;
		margin-bottom: 0.25rem;
	}
	.file {
		margin-top: 1rem;
		display: flex;
		gap: 1rem;
		flex-direction: column;
	}
	label {
		text-align: left;
		width: 140px;
		display: flex;
		align-items: center;
	}
	.textInput {
		border-radius: var(--border-radius-medium);
		background-color: var(--secondary-color);
		border: 2px solid var(--border-color);
		outline: none;
		padding: 0.5rem;
		width: 100%;
		transition-duration: 0.1s !important;
	}
	.textInput:focus {
		background-color: var(--accent-color-secondary);
	}
</style>
