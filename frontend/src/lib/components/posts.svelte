<script lang="ts">
	import { onMount } from 'svelte';
	import { get_posts, delete_post } from '$lib/requests';
	import { isUserLogged, refreshPosts } from '$lib/stores';

	let posts = ['empty'];
	let error: any = null;
	let deleting: boolean = false;

	/** @type {import('./$types').PageData} */
	export let data;

	async function load_posts() {
		try {
			const fetchedPosts = await get_posts();
			posts = fetchedPosts.reverse();
		} catch (err) {
			error = err;
		}
	}

	export async function del_post(
		title: string,
		description: string,
		path: string,
		time: Int16Array
	) {
		if (!deleting) {
			deleting = true;
			await delete_post(title, description, path, time).then((data) => {
				if (data['response']) {
					refreshPosts.set(!$refreshPosts);
				}
			});
		}
	}

	onMount(() => {
		load_posts();
	});
</script>

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
								on:click={del_post(post['name'], post['description'], post['source'], post['time'])}
								><i class="fa-solid fa-trash-can"></i></button
							>
						{/if}
					{/if}
				</div>
			</div>
			<div class="imageContainer">
				<img
					class="image"
					src={`http://127.0.0.1:5000/static/${post['source']}.jpg`}
					alt={`http://127.0.0.1:5000/static/${post['source']}.jpg`}
				/>
			</div>
			<div class="description">
				<p>{post['description']}</p>
			</div>
		</div>
		<!-- Adjust according to the actual structure of your post object -->
	{/each}
{/if}

<style>
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
</style>
