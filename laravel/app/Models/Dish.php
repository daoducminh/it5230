<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Dish extends Model
{
    use HasFactory;

    protected $fillable = [
        'dish_name',
        'description'
    ];

    protected $casts = [
        'ingredients' => 'array',
        'public' => 'boolean',
        'calories' => 'integer'
    ];

    public function menus()
    {
        return $this->belongsToMany(
            'App\Models\Menu',
            'menu_details',
            'dish_id',
            'menu_id'
        );
    }
}
