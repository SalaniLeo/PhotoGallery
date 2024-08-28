<script lang="ts">
	import { isUserLogged, refreshPosts, showCreatePost } from '$lib/stores';
	import { goto } from '$app/navigation';
	import Upload from '$lib/components/upload.svelte';

	let error: any = null;

	/** @type {import('./$types').PageData} */
	export let data;

	let posts = data['posts'].map((post: any) => ({ ...post, expand_image: false })); // Initialize expand_image for each post
	const addresses = data['addresses'];

	const url = addresses['url'];
	const delete_address = addresses['delete'];

	async function delete_post(title: string, description: string, path: string, time: number) {
		try {
			await fetch(delete_address, {
				method: 'POST',
				body: JSON.stringify({ title, description, path, time }),
				headers: {
					'Content-Type': 'application/json'
				}
			}).then((response) => {
				const updatedArray = posts.filter((item: { source: string }) => item.source !== path);
				posts = updatedArray;
				refreshPosts.set(!$refreshPosts);
				return response.json();
			});
		} catch (error) {
			console.error('Could not delete post: ', error);
		}
	}

	function toggleExpandImage(index: number) {
		posts = posts.map((post: { expand_image: any }, i: number) => {
			if (i === index) {
				return { ...post, expand_image: !post.expand_image };
			} else {
				return { ...post, expand_image: false };
			}
		});
	}
</script>

<div class="root">
	<div class="content">
		<div class="admin-actions">
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
					<div class="posts-container">
						{#each posts as post, index}
							<div class="post {post.id}" class:fullscreen_post={post.expand_image}>
								<div class="top">
									<div class="left"></div>
									<div class="title">
										<h2>{post['name']}</h2>
									</div>
									<div class="actions">
										<button
											id="enlarge_btn"
											class="button"
											on:click={() => toggleExpandImage(index)}
											><i
												class="fa-solid"
												class:fa-up-right-and-down-left-from-center={!post.expand_image}
												class:fa-down-left-and-up-right-to-center={post.expand_image}
											></i></button
										>
										<a
											href="{url}/static/{post['source']}.jpg"
											download={post['source']}
											class="button"
											id="download"><i class="fa-solid fa-download"></i></a
										>

										{#if $isUserLogged}
											{#if data.user?.admin}
												<button
													id="trash"
													class="button"
													on:click={async () => {
														const result = await delete_post(
															post.name,
															post.description,
															post.source,
															post.time
														);
													}}
												>
													<i class="fa-solid fa-trash-can"></i>
												</button>
											{/if}
										{/if}
									</div>
								</div>
								<div class="image-container">
									<img
										class="image"
										src={`${url}/posts/${post['source']}.jpg`}
										alt={`${url}/posts/${post['source']}.jpg`}
									/>
								</div>
								<div class="description">
									<p>{post['description']}</p>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			{/key}
		</div>
	</div>
	<Upload {data}></Upload>
</div>

<style>
	.content {
		display: flex;
		align-items: center;
		justify-self: center;
		flex-direction: column;
		width: 100%;
	}
	.posts-container {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		align-items: center;
	}
	.post {
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
		width: fit-content;
	}
	.post h2 {
		margin: 0px;
	}
	.post > div {
		margin: 0.5rem;
	}
	.post > .top {
		width: 100%;
		display: flex;
		flex-direction: row;
		margin-bottom: 0.5rem;
	}
	.post > .top > div {
		width: 100%;
		min-width: fit-content;
	}
	.post > .top > .title {
		min-width: max-content;
	}
	.post > .top > .actions {
		display: flex;
		justify-content: end;
		gap: 0.5rem;
	}
	.post > .description {
		width: 80%;
		max-width: 50vw;
		line-height: 1.25rem;
		text-align: center !important;
	}
	.post > .description > * {
		color: var(--font-secondary-color);
		margin: 0.5rem;
	}
	#trash {
		background-color: var(--font-error-color);
	}
	#download {
		max-height: 16px;
		width: 16px;
	}
	.post .image {
		display: block;
		max-width: 40vw;
		max-height: 33vh;
		width: auto;
		height: auto;
		overflow: hidden;
		border-radius: var(--border-radius-medium);
	}
	.post .image-container {
		margin: 0 !important;
	}
	.fullscreen_post .image {
		display: block;
		max-width: 70vw;
		max-height: 75vh;
		width: auto;
		height: auto;
		overflow: hidden;
		border-radius: var(--border-radius-medium);
	}
	.admin-actions {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 1rem;
		margin-bottom: 0.5rem;
	}

	@media screen and (max-width: 1200px) {
		.post .image {
			max-width: 50vw;
		}
	}
	@media screen and (max-width: 1000px) {
		.posts-container {
			display: flex;
			flex-direction: column;
			gap: 1rem;
			align-items: unset;
			padding: 1rem;
		}
		.post {
			border-radius: var(--border-radius-medium);
			transition-duration: 0s !important;
			width: unset;
		}
		.post > .top > div {
			width: 100%;
			min-width: unset;
		}
		.post .image {
			max-width: 60vw;
			border-radius: var(--border-radius-light);
		}
		.post > .top {
			flex-direction: column;
			margin-bottom: 1rem;
		}
		.post > .top > .actions {
			display: flex;
			justify-content: center;
			gap: 0.5rem;
		}
	}
	@media screen and (max-width: 720px) {
		.post * {
			transition-duration: 0s !important;
		}
		.fullscreen_post * {
			max-width: 100vw !important;
			transition-duration: 0s !important;
		}
		.fullscreen_post {
			background-color: var(--shadow-color-medium);
			backdrop-filter: blur(10px);
			width: 100vw;
			padding-left: 0px;
			padding-right: 0px;
			height: 100vh;
			position: fixed;
			top: 0px;
			left: 0px !important;
		}
		.fullscreen_post p,
		.fullscreen_post h2 {
			display: none;
		}
		.fullscreen_post .actions {
			margin-right: 1rem;
			margin-bottom: 1rem;
			transform: translateY(-100px);
		}
		.fullscreen_post .image {
			display: block;
			max-width: unset;
			max-height: unset;
			left: 0px;
			width: 100%;
			height: auto;
			overflow: hidden;
			transform: translateY(-100px);
			border-radius: var(--border-radius-medium);
		}
		.post > .description {
			width: unset;
			max-width: unset;
		}
	}
</style>
