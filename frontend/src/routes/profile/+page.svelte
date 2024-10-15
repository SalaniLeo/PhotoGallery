<script lang="ts">
	import Cookies from 'js-cookie';
	import AskPassword from '$lib/components/askPassword.svelte';
	import { isUserLogged, rootData } from '$lib/stores.js';
	import PostView from '$lib/components/postView.svelte';
	import changepfp from '$lib/components/images/changepfp.png';
	import { showToast } from '$lib';
	import { invalidateAll } from '$app/navigation';

	let showLiked = false;
	let showReacted = false;

	const findPosts = (posts: Array<{ id: string }>, likeDataArray: Array<object>) => {
		return likeDataArray.map((likeData: any) => posts.find((post) => post.id === likeData.post_id));
	};

	const findReactedPosts = (posts: Array<{ id: string }>, toFindDataArray: Array<object>) => {
		return toFindDataArray.map((toFindData: any) =>
			posts.find((post) => post.id === toFindData.id)
		);
	};

	let password: string;

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

	async function applyEdit() {
		try {
			if (password) {
				const response = await fetch($rootData.addresses.edit_profile, {
					method: 'POST',
					body: JSON.stringify({
						firstname: $rootData.user.info.firstname,
						lastname: $rootData.user.info.lastname,
						email: $rootData.user.info.email,
						password,
						user_id: $rootData.user.info.user_id,
						pfp: $rootData.user.info.pfp
					}),
					headers: {
						'Content-Type': 'application/json',
						'x-api-key': $rootData.apikey
					}
				});
				await response.json().then((data) => {
					showToast('Changes applied', data.status);

					Cookies.set('accessToken', data.user.accessToken);
					Cookies.set('refreshToken', data.user.refreshToken);
				});
			}
		} catch (error: any) {
			showToast(error, 400);
			console.error('Error validating password', error);
		}
	}

	async function deleteAccount() {
		let user_id = $rootData.user.info.user_id;
		try {
			await fetch($rootData.addresses.delete_account, {
				method: 'POST',
				body: JSON.stringify({
					user_id: user_id
				}),
				headers: {
					'Content-Type': 'application/json',
					'x-api-key': $rootData.apikey
				}
			});
			await logout();
		} catch (error: any) {
			showToast(error, 400);
		}
	}

	async function logout() {
		const response = await fetch('/auth/logout');

		if (response.ok) {
			isUserLogged.set(false);
			invalidateAll();
		} else {
			console.error('Logout failed');
		}
	}

	let showmodal1 = false;
	let loadingpasswd1 = false;
	let ispasswd1valid = false;

	let showmodal2 = false;
	let loadingpasswd2 = false;
	let ispasswd2valid = false;

	let showmodal3 = false;
	let loadingpasswd3 = false;
	let ispasswd3valid = false;
</script>

<div class="root">
	<div class="content flexrow space-between gap-large">
		<!-- <div class="profile-photo">
			<img bind:this={image} id="imagePreview" style="display: none;" alt="none" />
			{#if $rootData.user.info.pfp != 'default'}
				<img
					bind:this={$rootData.user.info.pfp}
					src=""
					id="stockpfp"
					alt=""
					width="300"
					height="300"
					style="cursor: pointer"
				/>
			{:else if image}
				<img src={image} id="stockpfp" alt="" width="300" height="300" style="cursor: pointer" />
			{:else}
				<img
					src={changepfp}
					id="stockpfp"
					alt=""
					width="300"
					height="300"
					style="cursor: pointer"
				/>
			{/if}
			<label for="pfpchanger" class="pfpchanger"> <i class="fa-solid fa-folder-open"></i> </label>
			<input bind:this={input} on:change={onChange} type="file" id="pfpchanger" />
		</div> -->
		<div class="profile-info">
			<div class="title">
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<h2>
					Info
					{#if !ispasswd1valid}
						<span
							style="cursor: pointer;"
							on:click={() => {
								showmodal1 = true;
								ispasswd2valid = false;
							}}><i class="fa-solid fa-pen-to-square"></i></span
						>
					{/if}
				</h2>
			</div>
			<div class="user-info">
				<div class="labels">
					<p class="secondary">Firstname:</p>
					<p class="secondary">Lastname:</p>
					<p class="secondary">Email:</p>
					<p class="secondary">Password:</p>
				</div>
				<div class="data">
					{#if ispasswd1valid}
						<div
							style="display: flex; flex-direction: column; align-items: start; justify-content: start; margin: 0;"
						>
							<input type="text" bind:value={$rootData.user.info.firstname} />
							<input type="text" bind:value={$rootData.user.info.lastname} />
							<input type="text" bind:value={$rootData.user.info.email} />
							<input type="text" bind:value={password} />
							<div class="applyUserDiv hendalign gap-medium">
								<button
									class="applyButton"
									on:click={() => {
										applyEdit();
										ispasswd1valid = false;
										password = '';
									}}><i class="fa-solid fa-check"></i></button
								>
								<button
									class="applyButton"
									on:click={() => {
										ispasswd1valid = false;
										password = '';
									}}><i class="fa-solid fa-xmark"></i></button
								>
							</div>
						</div>
					{:else}
						<p>{$rootData.user.info.firstname}</p>
						<p>{$rootData.user.info.lastname}</p>
						<p>{$rootData.user.info.email}</p>
						<div class="password flexrow gap-medium">
							{#if ispasswd2valid}
								<p>{password}</p>
								<button
									class="transparent"
									on:click={() => {
										ispasswd2valid = false;
									}}><i class="fa-solid fa-eye"></i></button
								>
							{:else}
								<p>...</p>
								<button
									class="transparent"
									on:click={() => {
										showmodal2 = true;
									}}><i class="fa-solid fa-eye-slash"></i></button
								>
							{/if}
						</div>
					{/if}
				</div>
			</div>
			<div class="title">
				<h2>User statistics</h2>
			</div>
			<div class="user-statistics">
				<div class="labels">
					<p class="onhover secondary">Liked posts:</p>
					<p class="onhover secondary">Reacted posts:</p>
				</div>
				<div class="data">
					<p class="onhover" style="display: flex; align-items: center; gap: 0.5rem;">
						{Object.keys($rootData.user.liked_posts).length}
						<button
							on:click={() => {
								if (showReacted) {
									showReacted = !showReacted;
								}
								showLiked = !showLiked;
							}}
							class="transparent"
							style="display: flex; align-items: center; gap: 0.5rem;"
						>
							{#if showLiked}
								<span class="secondary">Hide</span>
							{:else}
								<span class="secondary">View</span>
							{/if}
							<span class="fa-solid fa-caret-right show secondary" style="opacity: 0;"></span>
						</button>
					</p>
					<p class="onhover" style="display: flex; align-items: center; gap: 0.5rem;">
						{Object.keys($rootData.user.reacted_posts).length}
						<button
							on:click={() => {
								if (showLiked) {
									showLiked = !showLiked;
								}
								showReacted = !showReacted;
							}}
							class="transparent"
							style="display: flex; align-items: center; gap: 0.5rem;"
						>
							{#if showReacted}
								<span class="secondary">Hide</span>
							{:else}
								<span class="secondary">View</span>
							{/if}
							<span class="fa-solid fa-caret-right show secondary" style="opacity: 0;"></span>
						</button>
					</p>
					<!-- <p class="onhover">
							{Object.keys($rootData.user.reactions).length}
							<i class="fa-solid fa-caret-right show" style="opacity: 0;"></i>
						</p> -->
				</div>
			</div>
			<div class="title">
				<h2>Account actions</h2>
			</div>
			<div class="accout-actions">
				<div class="labels">
					<p class="secondary">Log out:</p>
					<p class="secondary">Delete account:</p>
				</div>

				<div class="data">
					<div class="logout-button">
						<div class="logout">
							<button on:click={logout} class="warningbackground warningonhover"
								><i class="fa-solid fa-right-from-bracket"></i></button
							>
						</div>
					</div>
					<div class="delete-button">
						{#if ispasswd3valid}
							<div class="confirm valign halign gap-medium">
								Are you sure?
								<button
									class="transparent okonhover padding1"
									on:click={() => {
										deleteAccount();
									}}><i class="fa-solid fa-check"></i></button
								>
								<button
									class="transparent erroronhover padding1"
									on:click={() => {
										ispasswd3valid = false;
										password = '';
									}}><i class="fa-solid fa-xmark"></i></button
								>
							</div>
						{:else}
							<button
								class="errorbackground erroronhover"
								on:click={() => {
									showmodal3 = true;
								}}><i class="fa-solid fa-trash-can"></i></button
							>
						{/if}
					</div>
				</div>
			</div>
		</div>
		<div class="more-info">
			{#if showLiked && !showReacted}
				<div class="posts_container flexcolumn gap-large valign">
					{#each findPosts($rootData.posts, $rootData.user.liked_posts) as post}
						<div class="post-wrapper">
							<PostView
								onlyDownload={true}
								{post}
								imageOnly={false}
								showButtons={true}
								showActions={true}
							></PostView>
						</div>
					{/each}
				</div>
			{/if}
			{#if showReacted && !showLiked}
				<div class="posts_container flexcolumn gap-large valign">
					{#each findReactedPosts($rootData.posts, $rootData.user.reacted_posts) as post}
						<div class="post-wrapper">
							<PostView
								onlyDownload={true}
								{post}
								imageOnly={false}
								showButtons={true}
								showActions={true}
							></PostView>
						</div>
					{/each}
				</div>
			{/if}
		</div>
	</div>
</div>

<AskPassword
	bind:showModal={showmodal1}
	bind:password
	bind:loading={loadingpasswd1}
	bind:valid={ispasswd1valid}
/>

<AskPassword
	bind:showModal={showmodal2}
	bind:password
	bind:loading={loadingpasswd2}
	bind:valid={ispasswd2valid}
/>

<AskPassword
	bind:showModal={showmodal3}
	bind:password
	bind:loading={loadingpasswd3}
	bind:valid={ispasswd3valid}
/>

<style>
	.accout-actions {
		height: unset;
	}
	.accout-actions > .labels {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}
	.accout-actions > .data {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}
	.accout-actions > .labels > p {
		height: 28px;
		margin-top: 0.5rem;
		margin-bottom: 0.5rem;
		display: flex;
		align-items: center;
	}
	.logout-button,
	.delete-button {
		height: 44px;
		margin: 0px !important;
	}
	.confirm {
		height: 100%;
	}
	.applyButton {
		padding: 0.25rem;
		width: 35px;
		height: 35px;
	}
	.applyUserDiv {
		width: 100%;
		padding-top: 0.5rem;
	}
	.data > div {
		margin-top: 1rem;
		margin-bottom: 1rem;
	}
	.error {
		color: var(--font-error-color);
	}
	input[type='text'] {
		margin-top: 1rem;
		padding: 0;
		height: 17.2px;
		width: 14rem;
	}
	.password p {
		margin: 0;
	}
	.pfpchanger {
		cursor: pointer;
		font-size: 4rem;
		opacity: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		position: absolute;
		transform: translateY(calc(-100% - 5px));
		width: 300px;
		height: 300px;
		border-radius: 50%;
	}
	.pfpchanger:hover {
		background-color: var(--background-blurry);
		opacity: 0.75;
	}
	.liked {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}
	.onhover:hover .show {
		opacity: 100 !important;
	}
	.user-info,
	.user-statistics,
	.accout-actions {
		display: flex;
		gap: 1rem;
	}
	#stockpfp {
		border-radius: 50%;
		height: auto;
	}
	@media screen and (max-width: 1000px) {
		#stockpfp {
			width: 175px;
		}
	}
</style>
