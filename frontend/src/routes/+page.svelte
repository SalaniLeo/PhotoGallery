<script lang="ts">
	import { isUserLogged, refreshPosts, showCreatePost } from '$lib/stores';
	import { goto } from '$app/navigation';
	import { currentTheme } from '$lib/theme';

	let error: any = null;

	/** @type {import('./$types').PageData} */
	export let data;

	let posts = data['posts'];
	const addresses = data['addresses'];

	const url = addresses['url'];
	const delete_address = addresses['delete'];
	const upload_address = addresses['upload'];

	let showModal = false;
	let dialog: HTMLDialogElement;
	let title: string, description: string;

	$: showCreatePost.subscribe((value) => {
		showModal = value;
		if (dialog) {
			value ? dialog.showModal() : dialog.close();
		}
	});

	let input: any;
	let image: any;
	let container;
	let showImage = false;
	let uploading = false;

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
		if (!uploading) {
			uploading = true;
			const file = input.files[0];
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
					body: formData
				});

				if (response.ok) {
					console.log(response);
					showCreatePost.set(!$showCreatePost);
					posts = await fetch(addresses['address'] + addresses['get_posts']);
					refreshPosts.set(!$refreshPosts);
				} else {
					console.error('Upload failed:', response.statusText);
				}
			} catch (error) {
				console.error('Error uploading the file:', error);
			} finally {
				uploading = false;
			}
		}
	}

	async function delete_post(title: string, description: string, path: string, time: number) {
		try {
			await fetch(delete_address, {
				method: 'POST',
				body: JSON.stringify({ title, description, path, time }),
				headers: {
					'Content-Type': 'application/json'
				}
			}).then((response) => {
				const updatedArray = posts.filter((item) => item.source !== path);
				posts = updatedArray;
				refreshPosts.set(!$refreshPosts);
				return response.json();
			});
		} catch (error) {
			console.error('Could not delete post: ', error);
		}
	}
</script>

<div class="root">
	<div class="content">
		<div class="top">
			{#if $isUserLogged}
				<p>Hi, {data.user?.name}!</p>
				{#if data.user?.admin}
					<button on:click={() => showCreatePost.set(true)}>Create Post</button>
				{/if}
				<button on:click={() => goto('/profile')}>Profile</button>
			{/if}
		</div>
		<div class="center">
			{#key $refreshPosts}
				{#if error}
					<p style="color: red">{error.message}</p>
				{:else if posts[0] == 'empty'}
					<p>Loading posts...</p>
				{:else if posts.length < 1}
					<p>No posts have been uploaded</p>
				{:else}
					{#each posts as post}
						<div class="post">
							<div class="top">
								<div class="title">
									<h2>{post['name']}</h2>
								</div>
								<div class="actions">
									{#if $isUserLogged}
										{#if data.user?.admin}
											<button
												class="trash"
												on:click={async () => {
													const result = await delete_post(
														post.name,
														post.description,
														post.source,
														post.time
													);
													console.log('Post deleted:', result);
												}}
											>
												<i class="fa-solid fa-trash-can"></i>
											</button>
										{/if}
									{/if}
								</div>
							</div>
							<div class="imageContainer">
								<img
									class="image"
									src={`${url}/static/${post['source']}.jpg`}
									alt={`${url}/static/${post['source']}.jpg`}
								/>
							</div>
							<div class="description">
								<p>{post['description']}</p>
							</div>
						</div>
					{/each}
				{/if}
			{/key}
		</div>
	</div>

	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
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
</div>

<style>
	.content {
		display: flex;
		align-items: center;
		justify-self: center;
		flex-direction: column;
		width: 100%;
	}
	.top {
		margin-bottom: 1rem;
	}

	.post {
		margin-bottom: 1rem;
		padding: 1rem;
		padding-left: 2rem;
		padding-right: 2rem;
		border-radius: var(--border-radius-heavy);
		background-color: var(--secondary-color);
		box-shadow: var(--shadow-color-medium) 0px 0px 10px;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	.post h2 {
		margin: 0px;
	}
	.post > div {
		margin: 0.5rem;
	}
	.trash {
		background-color: var(--font-error-color);
		height: 40px;
		width: 40px;
	}
	.image {
		display: block;
		max-width: 40vw;
		max-height: 33vh;
		width: auto;
		height: auto;
		overflow: hidden;
		border-radius: var(--border-radius-medium);
	}
	.description {
		line-height: 1.25rem;
		text-align: center;
	}
	.description > * {
		color: var(--font-secondary-color);
	}
	@media screen and (max-width: 1200px) {
		.image {
			max-width: 50vw;
		}
	}
	@media screen and (max-width: 1000px) {
		.post {
			border-radius: var(--border-radius-medium);
		}
		.image {
			max-width: 60vw;
			border-radius: var(--border-radius-light);
		}
	}
	@media screen and (max-width: 720px) {
		.image {
			max-width: 100%;
		}
	}
	dialog {
		background-color: var(--primary-color);
		border-radius: var(--border-radius-heavy);
		border: none;
		padding: 0;
		width: max-content;
		height: fit-content;
		outline: 2px solid var(--accent-color-primary);
	}
	dialog::backdrop {
		background: rgba(0, 0, 0, 0.3);
		backdrop-filter: blur(4px);
	}
	.dialog-content {
		padding: 1em;
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
	.center {
		min-width: 400px;
		min-height: 300px;
	}
	img {
		max-width: 500px;
		max-height: 500px;
	}
	.name,
	.description {
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
		outline: none;
		border: none;
		padding: 10px;
		width: 100%;
		transition-duration: 0.25s;
	}
	.textInput:focus {
		background-color: var(--accent-color-secondary);
	}
</style>
